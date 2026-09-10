"""Generate original SVG illustrations from the checked repository wiring contract."""

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/figures"
COLORS = {
    "power": "#c94348",
    "ground": "#263744",
    "data": "#22865d",
    "analog": "#d88a12",
    "CS": "#4168c1",
    "SCK": "#7654ac",
    "MISO": "#078b9d",
    "MOSI": "#4366a0",
}


def _canonical_pin(pin: str) -> str:
    """Normalize Wokwi part ids and SPI pin aliases to the firmware contract."""
    part, signal = pin.split(":", 1)
    if part.startswith("dht"):
        part = "dht"
    elif part in {"pullup", "r1", "dht_pullup"}:
        part = "pullup"
    elif part in {"joystick", "potentiometer", "gas_analog"} and signal in {"VERT", "SIG", "AO"}:
        part, signal = "gas", "AO"
    if part == "sd":
        signal = {"DO": "MISO", "DI": "MOSI"}.get(signal, signal)
    return f"{part}:{signal}"


def _canonical_edge(a: str, b: str) -> frozenset[str]:
    return frozenset((_canonical_pin(a), _canonical_pin(b)))


def wiring() -> dict:
    """Extract and cross-check pins; refuse to draw a stale wiring contract."""
    diagram = json.loads((ROOT / "wokwi/diagram.json").read_text())
    edges = {_canonical_edge(row[0], row[1]) for row in diagram["connections"]}
    config = (ROOT / "firmware/include/Config.h").read_text()
    pins = {
        key: int(re.search(rf"\b{key}\s*=\s*(\d+)", config)[1])
        for key in ("DHT_PIN", "GAS_PIN", "SD_CS", "SAMPLE_MS")
    }
    expected = [
        ("dht:SDA", f"esp:D{pins['DHT_PIN']}"),
        ("gas:AO", f"esp:D{pins['GAS_PIN']}"),
        ("sd:CS", f"esp:D{pins['SD_CS']}"),
        ("sd:SCK", "esp:D18"),
        ("sd:MISO", "esp:D19"),
        ("sd:MOSI", "esp:D23"),
        ("dht:VCC", "esp:3V3"),
        ("sd:VCC", "esp:3V3"),
        ("gas:VCC", "esp:VIN"),
        ("dht:GND", "esp:GND.1"),
        ("gas:GND", "esp:GND.1"),
        ("sd:GND", "esp:GND.1"),
        ("pullup:1", "esp:3V3"),
        ("pullup:2", "dht:SDA"),
    ]
    for a, b in expected:
        if _canonical_edge(a, b) not in edges:
            raise ValueError(f"Review changed wiring before drawing: {a} -> {b}")
    # Logger uses Arduino ESP32's default SPI bus; do not invent an explicit SPI.begin call.
    if "SD.begin(Config::SD_CS)" not in (ROOT / "firmware/src/Logger.cpp").read_text():
        raise ValueError("Review the storage interface before drawing.")
    return pins


class SVG:
    def __init__(self, width: int, height: int, title: str, subtitle: str):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
            "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#193948} .small{fill:#516b77}</style>",
        ]
        self.rect(0, 0, width, height, "#f5f8fa", radius=0)
        self.text(36, 44, title, 26, weight="bold")
        self.text(36, 73, subtitle, 15)

    def rect(self, x, y, w, h, fill="white", stroke="none", radius=10):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'
        )

    def text(self, x, y, label, size=16, weight="normal", color=None, anchor="start"):
        style = f' style="fill:{color}"' if color else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{style}>{escape(str(label))}</text>'
        )

    def line(self, points, color, width=3, dashed=False):
        self.parts.append(
            f'<polyline points="{" ".join(f"{x},{y}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'
            + (' stroke-dasharray="6 5"' if dashed else "")
            + "/>"
        )

    def dot(self, x, y, color, r=4):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.parts) + "\n</svg>\n", encoding="utf-8")


def module(s, kind, x, y, w=220, h=240):
    """Illustrative component bodies; connector callouts are functional, not package pin order."""
    if kind == "DHT22":
        s.rect(x, y, w, h, "#fff", "#b8c6cc")
        for yy in range(int(y + 25), int(y + h - 55), 18):
            s.rect(x + 20, yy, w - 40, 7, "#d1dce1", radius=3)
        s.text(x + w / 2, y + h - 22, "DHT22", 19, "bold", anchor="middle")
    elif kind == "ESP32":
        s.rect(x, y, w, h, "#23434e", "#132e37")
        s.rect(x + 34, y + 24, w - 68, h - 84, "#cad5db", "#94a8b1")
        s.rect(x + 50, y + 35, w - 100, 35, "#294853", radius=2)
        for xx in range(int(x + 60), int(x + w - 55), 20):
            s.line([(xx, y + 62), (xx, y + 42), (xx + 10, y + 42), (xx + 10, y + 62)], "#ccba75", 2)
        s.text(x + w / 2, y + 112, "ESP32", 25, "bold", anchor="middle")
        s.text(x + w / 2, y + 139, "WiFi · ADC · SPI", 14, anchor="middle")
        s.rect(x + w / 2 - 24, y + h - 49, 48, 35, "#c8d4da", "#829ba7", 3)
        s.rect(x + w / 2 - 16, y + h - 40, 32, 17, "#304b56", radius=2)
        for yy in range(int(y + 18), int(y + h - 15), 20):
            s.rect(x + 8, yy, 10, 9, "#ddc775", radius=1)
            s.rect(x + w - 18, yy, 10, 9, "#ddc775", radius=1)
    elif kind == "MQ-2":
        s.rect(x, y, w, h, "#214e70", "#193c58")
        s.dot(x + w / 2, y + 82, "#c4d0d6", 64)
        s.dot(x + w / 2, y + 82, "#e1e8ec", 53)
        for dx in range(-32, 33, 12):
            for dy in range(-32, 33, 12):
                s.dot(x + w / 2 + dx, y + 82 + dy, "#a2b3bc", 2)
        s.rect(x + 24, y + h - 62, 40, 28, "#e3d5a4", radius=3)
        s.dot(x + 44, y + h - 48, "#667e8a", 7)
        s.text(x + w / 2 + 15, y + h - 33, "MQ-2", 20, "bold", color="#fff", anchor="middle")
    else:
        s.rect(x, y, w, h, "#254e64", "#193c50")
        s.rect(x + 23, y + 35, w - 46, h - 87, "#cbd7de", "#849aa6", 4)
        s.rect(x + 38, y + 48, w - 76, 43, "#172f3b", radius=2)
        s.text(x + w / 2, y + 126, "microSD", 21, "bold", anchor="middle")
        s.text(x + w / 2, y + h - 25, "SPI storage", 17, color="#fff", anchor="middle")


def overview(pins):
    s = SVG(
        1400,
        850,
        "Virtual hardware · acquisition node",
        "Virtual hardware layout derived from the project wiring configuration. Synthetic demonstrator; not physical validation.",
    )
    s.rect(28, 103, 1344, 677, "#fff", "#dde6eb", 14)
    # A restrained breadboard field behind routed wires.
    for x in range(60, 1350, 22):
        for y in range(530, 727, 22):
            s.dot(x, y, "#e7edf1", 1.6)
    for y, label in [
        (137, "3.3 V · DHT22 + microSD"),
        (173, "VIN / 5 V · MQ-2, simulator only"),
        (209, "GND · common return"),
    ]:
        c = COLORS["ground" if y == 209 else "power"]
        s.line([(50, y), (1335, y)], c, 3)
        s.rect(45, y - 25, 285, 21, "#fff", radius=2)
        s.text(50, y - 9, label, 15, color=c)
    specs = [
        ("DHT22", 90, 250, 210),
        ("ESP32", 475, 250, 300),
        ("MQ-2", 855, 250, 210),
        ("microSD", 1130, 250, 210),
    ]
    for kind, x, y, w in specs:
        module(s, kind, x, y, w, 230)
    # Top functional power contacts, drawn as callouts rather than literal connector order.
    for x, rail, label in [
        (115, 137, "VCC"),
        (275, 209, "GND"),
        (500, 137, "3V3"),
        (625, 173, "VIN"),
        (750, 209, "GND"),
        (880, 173, "VCC"),
        (1040, 209, "GND"),
        (1155, 137, "VCC"),
        (1315, 209, "GND"),
    ]:
        c = COLORS["ground" if rail == 209 else "power"]
        if x == 115:
            s.line([(x, 250), (x, 225), (335, 225), (335, rail)], c, 2)
            s.dot(335, rail, c)
        else:
            s.line([(x, 250), (x, rail)], c, 2)
            s.dot(x, rail, c)
        s.dot(x, 250, c)
        s.rect(x - 18, 230, 36, 16, "#fff", radius=2)
        s.text(x, 242, label, 12, anchor="middle")
    # Signals: no junction at wire crossings. A dot denotes an endpoint only.
    routes = [
        (170, 500, 550, "data", f"DATA → GPIO{pins['DHT_PIN']}"),
        (975, 545, 580, "analog", f"AO → GPIO{pins['GAS_PIN']}"),
        (1160, 590, 610, "CS", f"CS → GPIO{pins['SD_CS']}"),
        (1205, 635, 640, "SCK", "SCK → GPIO18"),
        (1250, 680, 670, "MISO", "MISO → GPIO19"),
        (1295, 725, 700, "MOSI", "MOSI → GPIO23"),
    ]
    for source, target, lane, key, label in routes:
        c = COLORS[key]
        s.line([(source, 480), (source, lane), (target, lane), (target, 480)], c, 3)
        s.dot(source, 480, c)
        s.dot(target, 480, c)
        s.text(185 if key == "data" else 800, lane - 8, label, 15, "bold", color=c)
        for x, name in [(source, label.split(" → ")[0]), (target, label.split("GPIO")[-1])]:
            s.rect(x - 18, 486, 36, 18, "#fff", radius=2)
            s.text(x, 500, name, 11, "bold", anchor="middle")
    # Pull-up is part of the actual DHT connection.
    s.line([(170, 550), (355, 550), (355, 285)], COLORS["data"], 2)
    s.rect(347, 256, 16, 29, "#efdfbb", "#9c8253", 2)
    s.line([(355, 256), (355, 137)], COLORS["power"], 2)
    s.dot(355, 137, COLORS["power"])
    s.dot(355, 550, COLORS["data"])
    s.text(369, 277, "10 kΩ pull-up", 14)
    s.text(
        50,
        755,
        "Functional pin callouts, not a physical pin-order or assembly drawing. DHT22 NC and MQ-2 DO are unused.",
        15,
    )
    s.text(
        36,
        808,
        "Wire colors are for visual clarity only. See the pin map and physical front-end note before interpreting this layout.",
        15,
    )
    s.save("virtual_hardware_overview.svg")


def connections(pins):
    s = SVG(
        1200,
        770,
        "ESP32 · exact interface connections",
        "Signal names and power nets extracted from diagram.json and checked against firmware configuration.",
    )
    s.rect(35, 108, 380, 568, "#fff", "#dce5eb")
    s.rect(805, 108, 360, 568, "#eaf1f5", "#cfdee6")
    s.text(58, 144, "PERIPHERAL CONTACT", 17, "bold")
    s.text(830, 144, "ESP32 CONNECTION", 17, "bold")
    rows = [
        ("DHT22 · DATA", f"GPIO{pins['DHT_PIN']}", "data"),
        ("MQ-2 · AO", f"GPIO{pins['GAS_PIN']} / ADC1", "analog"),
        ("microSD · CS", f"GPIO{pins['SD_CS']}", "CS"),
        ("microSD · SCK", "GPIO18", "SCK"),
        ("microSD · DO / MISO", "GPIO19", "MISO"),
        ("microSD · DI / MOSI", "GPIO23", "MOSI"),
        ("DHT22 + microSD · VCC", "3.3 V", "power"),
        ("MQ-2 · VCC", "VIN / 5 V (virtual only)", "power"),
        ("DHT22 + MQ-2 + SD · GND", "GND", "ground"),
    ]
    for i, (left, right, key) in enumerate(rows):
        y = 190 + i * 51
        s.text(58, y + 5, left, 17)
        s.text(830, y + 5, right, 17, "bold")
        s.line([(415, y), (805, y)], COLORS[key], 3)
        s.dot(415, y, COLORS[key])
        s.dot(805, y, COLORS[key])
    s.text(
        36,
        707,
        "DHT22: 10 kΩ pull-up from DATA to 3.3 V. NC unused. MQ-2 DO unused. UART serial monitor: 115200 baud.",
        15,
    )
    for x, label, key in [
        (36, "Power", "power"),
        (170, "Ground", "ground"),
        (310, "Digital", "data"),
        (450, "Analog", "analog"),
        (590, "SPI: CS / SCK / MISO / MOSI", "CS"),
    ]:
        s.line([(x, 742), (x + 22, 742)], COLORS[key], 4)
        s.text(x + 30, 747, label, 14)
    s.text(1160, 747, "Colors are not a standard.", 13, anchor="end")
    s.save("esp32_pin_connections.svg")


def components():
    s = SVG(
        1400,
        710,
        "Prototype components · roles and interfaces",
        "Original schematic-style illustrations; component shapes and connector locations are illustrative.",
    )
    specs = [
        (
            "ESP32",
            "ESP32 DevKit",
            ["Microcontroller and", "acquisition node"],
            ["GPIO4 · GPIO34", "SPI: GPIO5 / 18 / 19 / 23", "3V3 · VIN · GND"],
        ),
        (
            "DHT22",
            "DHT22",
            ["Virtual temperature and", "relative-humidity sensor"],
            ["VCC · DATA · NC · GND", "DATA has a 10 kΩ pull-up", "NC is not connected"],
        ),
        (
            "MQ-2",
            "MQ-2",
            ["Virtual analog", "gas-sensor surrogate"],
            ["VCC · GND · DO · AO", "AO → ADC; DO unused", "No selective NH₃ measurement"],
        ),
        (
            "microSD",
            "microSD module",
            ["Local CSV", "data logging"],
            ["VCC · GND · MISO · MOSI", "SCK · CS", "DO = MISO; DI = MOSI"],
        ),
    ]
    for i, (kind, title, role, labels) in enumerate(specs):
        x = 30 + i * 345
        s.rect(x, 112, 315, 485, "#fff", "#dce5eb")
        s.text(x + 20, 148, title, 23, "bold")
        module(s, kind, x + 67, 176, 180, 210)
        for j, text in enumerate(role):
            s.text(x + 20, 425 + j * 23, text, 18, "bold")
        for j, text in enumerate(labels):
            s.text(x + 20, 505 + j * 26, text, 15)
    s.text(
        36, 644, "MQ-2 is used only to demonstrate an analog gas-acquisition channel.", 18, "bold"
    )
    s.text(
        36,
        674,
        "It is not treated as a selective NH₃ sensor. All component views describe a virtual prototype, not tested hardware.",
        17,
    )
    s.save("prototype_components.svg")


def chain():
    s = SVG(
        1400,
        660,
        "Measurement chain · acquire, retain, communicate",
        "Conceptual chain with separate implementations: Python offline twin and ESP32/Wokwi acquisition demonstrator.",
    )
    labels = [
        ("Livestock", "environment", "Synthetic conditions"),
        ("Environmental", "and gas sensors", "Virtual / surrogate"),
        ("ESP32", "acquisition", "Time + raw signals"),
        ("QA/QC", "checks", "Preserve raw + flags"),
        ("Local logging", "microSD / CSV", "If storage healthy"),
        ("Telemetry", "queue", "Volatile records"),
        ("MQTT", "optional cloud", "Separate publisher"),
        ("Digital-twin", "dashboard", "Python state model"),
    ]
    for i, (a, b, c) in enumerate(labels):
        x = 30 + i * 172
        s.rect(x, 130, 154, 150, "#fff", "#d1dfe6")
        s.text(x + 15, 159, f"{i + 1:02}", 14, "bold", color="#577b8c")
        s.text(x + 77, 195, a, 16, "bold", anchor="middle")
        s.text(x + 77, 218, b, 16, "bold", anchor="middle")
        s.text(x + 77, 254, c, 12, anchor="middle")
        if i < 7:
            s.line([(x + 157, 205), (x + 168, 205)], "#577b8c", 2)
            s.line([(x + 164, 201), (x + 168, 205), (x + 164, 209)], "#577b8c", 2)
    s.text(
        36,
        318,
        "Logging and queueing are independent branches after QA/QC; a storage fault does not gate telemetry.",
        17,
    )
    s.rect(30, 347, 1340, 200, "#eaf1f5", "#d1dfe6")
    s.text(50, 382, "CONTROLLED PYTHON NETWORK-OUTAGE PATH", 17, "bold")
    stages = [
        ("Network", "unavailable"),
        ("Acquisition", "continues"),
        ("Local storage", "if healthy"),
        ("Telemetry", "remains queued"),
        ("Network", "restored"),
        ("Simulated receiver", "synchronizes queue"),
    ]
    for i, (a, b) in enumerate(stages):
        x = 50 + i * 220
        s.text(x, 429, a, 17, "bold")
        s.text(x, 455, b, 16)
        if i < 5:
            s.text(x + 190, 443, "→", 20)
    s.text(
        50,
        516,
        "Controlled simulation demonstrates retention of queued records during the tested outage.",
        17,
    )
    s.text(
        36,
        588,
        "No live ESP32 → Streamlit bridge is implemented. Firmware uses bounded RAM and QoS 0; delivery is not guaranteed.",
        16,
    )
    s.text(
        36,
        619,
        "Optional ThingsBoard is independent of the offline interview. Physical validation has not been performed.",
        16,
    )
    s.save("measurement_chain.svg")


def main():
    pins = wiring()
    overview(pins)
    connections(pins)
    components()
    chain()


if __name__ == "__main__":
    main()

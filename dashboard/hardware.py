"""Hardware presentation and a live view of the Python measurement chain."""

from html import escape
from pathlib import Path

import streamlit as st

from tools.generate_figures import wiring


def glance(twin, running: bool) -> None:
    """Render current simulation state, not physical-device connectivity."""
    last = twin.records[-1]
    cards = [
        (
            "Sensors",
            f"T/RH: {last['environmental_sensor_status']}",
            f"Gas: {last['gas_channel_status']}",
        ),
        (
            "ESP32 role",
            "ACQUIRING" if running else "PAUSED",
            f"Virtual scheduler · {len(twin.records)} attempts",
        ),
        (
            "Local storage",
            "LOGGING" if twin.storage == "OK" else "WRITE FAILURE",
            f"{len(twin.local_ids)} recorded · {len(twin.local_pending)} pending",
        ),
        ("Telemetry", twin.network, f"{len(twin.pending)} queued · {len(twin.delivered)} received"),
        ("Dashboard", "CURRENT SIMULATION STATE", f"Quality: {last['quality_flags']}"),
    ]
    st.markdown("#### System at a Glance")
    st.caption(
        "Live Python simulation state. ESP32 and microSD are represented roles; no physical device is connected."
    )
    html = '<style>.chain-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:18px}.chain-card{background:white;border:1px solid #dce5eb;border-radius:9px;padding:14px;overflow-wrap:anywhere}.chain-card h4{font-size:16px;margin:0 0 8px}.chain-card p{font-size:13px;margin:4px 0;color:#345464}@media(max-width:1000px){.chain-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:550px){.chain-grid{grid-template-columns:1fr}}</style><div class="chain-grid">'
    for i, (title, status, detail) in enumerate(cards):
        html += f'<div class="chain-card"><h4>{escape(title)} {"→" if i < 4 else ""}</h4><p><b>{escape(status)}</b></p><p>{escape(detail)}</p></div>'
    st.markdown(html + "</div>", unsafe_allow_html=True)


def hardware_page(root: Path) -> None:
    pins = wiring()
    st.markdown(
        "<style>[data-testid=stTable] table{table-layout:fixed;width:100%}[data-testid=stTable] th,[data-testid=stTable] td{overflow-wrap:anywhere}</style>",
        unsafe_allow_html=True,
    )
    st.write("Virtual hardware layout derived from the project wiring configuration.")
    st.caption(
        "ESP32/Wokwi is a separate acquisition demonstrator. This page does not show a live hardware connection."
    )
    st.image(str(root / "docs/figures/virtual_hardware_overview.svg"), width="stretch")
    st.caption(
        "Functional connection callouts, not physical package pin order. MQ-2 demonstrates a generic analog gas channel only."
    )
    rows = [
        [
            "DHT22",
            "Digital single-wire",
            f"GPIO{pins['DHT_PIN']}; 3.3 V / GND",
            "Temperature and relative humidity",
        ],
        [
            "MQ-2 surrogate",
            "Analog ADC1",
            f"GPIO{pins['GAS_PIN']}; VIN / 5 V / GND",
            "Analog acquisition; no selective NH₃ measurement",
        ],
        [
            "microSD module",
            "SPI",
            f"CS {pins['SD_CS']} · SCK 18 · MISO 19 · MOSI 23; 3.3 V / GND",
            "Local CSV records",
        ],
    ]
    headings = ["Component", "Interface", "ESP32 connection", "Purpose"]
    table = '<style>.hardware-map{width:100%;table-layout:fixed;border-collapse:collapse}.hardware-map th,.hardware-map td{white-space:normal!important;overflow-wrap:anywhere;border:1px solid #dce5eb;padding:10px;text-align:left;font-size:14px}.hardware-map th{background:#eaf1f5}@media(max-width:550px){.hardware-map thead{display:none}.hardware-map tr{display:block;margin-bottom:12px}.hardware-map td{display:block}.hardware-map td:before{content:attr(data-label) ": ";font-weight:bold}}</style><table class="hardware-map"><thead><tr>'
    table += "".join(f"<th>{heading}</th>" for heading in headings) + "</tr></thead><tbody>"
    for row in rows:
        table += (
            "<tr>"
            + "".join(
                f'<td data-label="{heading}">{escape(value)}</td>'
                for heading, value in zip(headings, row)
            )
            + "</tr>"
        )
    st.markdown(table + "</tbody></table>", unsafe_allow_html=True)
    st.write(
        "The ESP32 reads environmental measurements, attaches time and quality information, stores records locally and prepares telemetry for transmission. The Python twin demonstrates these operational roles independently, using synthetic NH₃ and local CSV files."
    )
    st.info(
        "The virtual analog connection demonstrates the acquisition path. A physical implementation requires verification of sensor output voltage, ESP32 ADC input range, source impedance, filtering, protection and calibration."
    )
    with st.expander("Exact pin connections", expanded=True):
        st.image(str(root / "docs/figures/esp32_pin_connections.svg"), width="stretch")
        st.download_button(
            "Download pin diagram (SVG)",
            (root / "docs/figures/esp32_pin_connections.svg").read_bytes(),
            "esp32_pin_connections.svg",
            "image/svg+xml",
        )
    with st.expander("Component reference"):
        st.image(str(root / "docs/figures/prototype_components.svg"), width="stretch")
    with st.expander("Technical interface details"):
        st.write(
            f"Firmware sampling interval: {pins['SAMPLE_MS'] / 1000:g} s. DHT22 DATA has a 10 kΩ pull-up to 3.3 V; NC is unused. MQ-2 AO feeds GPIO34; DO is unused. SPI uses Arduino ESP32 default bus pins (18/19/23) and CS GPIO5."
        )
        st.write(
            "Storage: SPI microSD, /measurements-v2.csv. Serial monitor: 115200 baud. WiFi carries optional MQTT; the broker is unconfigured by default. The firmware queue has 120 volatile slots and QoS 0 does not prove delivery. ADC counts leave analog sensor health UNVERIFIED."
        )
        st.write(
            "Wire colors are presentation choices, not electrical standards. The simulator-only 5 V analog path is not a validated physical circuit. No live ESP32-to-Streamlit bridge is implemented."
        )

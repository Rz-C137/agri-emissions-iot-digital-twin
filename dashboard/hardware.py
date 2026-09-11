"""Compact hardware and architecture presentation for the interview dashboard."""

from pathlib import Path

import streamlit as st

PIN_ROWS = [
    ("DHT22", "Digital", "GPIO4", "Virtual / firmware"),
    ("DS18B20", "1-Wire", "GPIO15", "Virtual / firmware"),
    ("BMP180", "I2C", "GPIO21 / GPIO22", "Virtual / firmware"),
    ("MQ-2 surrogate", "ADC", "GPIO34", "Simulation only"),
    ("microSD", "SPI", "CS 5; SCK 18; MISO 19; MOSI 23", "Firmware / virtual"),
    ("RS-485", "UART2", "RX 16; TX 17; DE/RE 27", "Software; physical pending"),
]


def _sensor_card(name: str, role: str, interface: str, status: str) -> str:
    return (
        '<div style="background:#fff;border:1px solid #dce5eb;border-top:3px solid #147d72;'
        'border-radius:7px;padding:10px;min-height:105px">'
        f'<strong style="color:#173f43">{name}</strong>'
        f'<div style="font-size:12px;color:#345464;margin-top:5px">{role}</div>'
        f'<div style="font-size:12px;margin-top:5px"><b>{interface}</b></div>'
        f'<div style="font-size:12px;color:#147d72;margin-top:5px">{status}</div>'
        "</div>"
    )


def _system_diagram() -> str:
    return """<svg viewBox="0 0 1200 360" role="img" aria-label="Bench to barn architecture" style="width:100%;background:#f8fbfc;border:1px solid #dce5eb;border-radius:8px">
    <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#147d72"/></marker></defs>
    <style>text{font-family:Arial,sans-serif;fill:#173f43}.label{font-size:16px;font-weight:bold}.small{font-size:13px;fill:#345464}.box{fill:#fff;stroke:#b8ccd2;stroke-width:2}.arrow{stroke:#147d72;stroke-width:3;fill:none;marker-end:url(#arrow)}</style>
    <rect class="box" x="25" y="110" width="180" height="130" rx="9" fill="#e8f3ef"/><text class="label" x="55" y="150">Barn context</text><text class="small" x="55" y="178">service / exhaust area</text><text class="small" x="55" y="204">environmental inputs</text>
    <rect class="box" x="260" y="75" width="220" height="200" rx="9"/><text class="label" x="295" y="115">ESP32 node</text><text class="small" x="295" y="145">sensors + acquisition</text><text class="small" x="295" y="170">QA/QC + fault flags</text><text class="small" x="295" y="195">local scheduler</text><text class="small" x="295" y="220">microSD + UART</text>
    <rect class="box" x="535" y="45" width="200" height="90" rx="9"/><text class="label" x="570" y="82">Local storage / QA</text><text class="small" x="570" y="108">CSV · flags · timestamps</text>
    <rect class="box" x="535" y="180" width="200" height="90" rx="9"/><text class="label" x="570" y="217">RS-485 reference</text><text class="small" x="570" y="243">Modbus bench path</text>
    <rect class="box" x="790" y="105" width="360" height="150" rx="9"/><text class="label" x="830" y="145">MQTT / dashboard</text><text class="small" x="830" y="175">receiver · validation · maintenance</text><text class="small" x="830" y="201">Streamlit virtual commissioning</text><text class="small" x="830" y="227">future central storage</text>
    <path class="arrow" d="M205 175 H260"/><path class="arrow" d="M480 135 H535"/><path class="arrow" d="M480 220 H535"/><path class="arrow" d="M480 245 C635 325 720 290 790 220"/><path class="arrow" d="M735 90 C780 80 790 125 790 145"/>
    </svg>"""


def _pcb_concept() -> str:
    return """<svg viewBox="0 0 900 300" role="img" aria-label="Prototype carrier PCB concept" style="width:100%;background:#102b2b;border-radius:8px">
    <style>text{font-family:Arial,sans-serif;fill:#eff9f4}.board{fill:#1a6256;stroke:#9dd5b9;stroke-width:3}.part{fill:#d9a441;stroke:#fff0b8;stroke-width:2}.conn{fill:#374b5a;stroke:#b9d0d8;stroke-width:2}.trace{stroke:#e8c46b;stroke-width:4;fill:none}.small{font-size:13px}.title{font-size:19px;font-weight:bold}</style>
    <rect class="board" x="55" y="35" width="790" height="225" rx="12"/><text class="title" x="85" y="70">Prototype carrier PCB concept · design stage</text>
    <rect class="conn" x="90" y="110" width="125" height="70" rx="5"/><text x="112" y="143">Power in</text><text class="small" x="112" y="164">protection/regulator</text>
    <rect class="part" x="345" y="95" width="190" height="110" rx="8"/><text x="390" y="145">ESP32 DevKit</text><text class="small" x="390" y="166">headers + USB</text>
    <rect class="conn" x="660" y="95" width="140" height="45" rx="5"/><text x="686" y="123">RS-485 A/B</text><rect class="conn" x="660" y="155" width="140" height="45" rx="5"/><text x="695" y="183">Sensor IO</text>
    <path class="trace" d="M215 145 H345 M535 120 H660 M535 175 H660"/><text class="small" x="85" y="230">Hand solder: headers, terminals, pull-up, LED and transceiver module pads.</text>
    </svg>"""


def _modbus_summary(root: Path) -> None:
    with st.expander("Advanced: Modbus protocol test", expanded=False):
        st.caption("Software protocol exercise only; physical RS-485 remains pending.")
        from dashboard.commissioning import commissioning_page

        commissioning_page(root)


def hardware_page(root: Path, twin, running: bool) -> None:
    """Render one linear hardware, Wokwi and bench architecture page."""
    st.caption("VIRTUAL / DESIGN-STAGE EVIDENCE · no physical device is connected")

    st.markdown("### A. System at a glance")
    st.write(
        "A compact ESP32 node acquires environmental signals, attaches QA/QC, stores records locally, and exposes software communication paths."
    )
    cards = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:8px">'
    cards += _sensor_card("DHT22", "Temperature + RH", "Digital · GPIO4", "Virtual / firmware")
    cards += _sensor_card(
        "DS18B20", "Independent temperature", "1-Wire · GPIO15", "Virtual / firmware"
    )
    cards += _sensor_card(
        "BMP180", "Temperature + pressure", "I2C · GPIO21/22", "Virtual / firmware"
    )
    cards += _sensor_card("MQ-2", "Analog gas surrogate", "ADC · GPIO34", "Simulation only")
    cards += _sensor_card("SCD41", "Phase 2 CO2/T/RH", "I2C · 0x62", "Bench pending")
    st.markdown(cards + "</div>", unsafe_allow_html=True)
    st.image(
        str(root / "docs/figures/virtual_hardware_overview.svg"),
        caption="One virtual ESP32 node view; Wokwi wiring source is `wokwi/diagram.json`.",
        width="stretch",
    )

    st.markdown("### B. Exact integration")
    st.image(str(root / "docs/figures/esp32_pin_connections.svg"), width="stretch")
    st.caption(
        "One authoritative virtual pin diagram derived from `firmware/include/Config.h` and `wokwi/diagram.json`."
    )
    st.dataframe(
        [
            {"Component": c, "Interface": i, "ESP32 pin": p, "Evidence status": s}
            for c, i, p, s in PIN_ROWS
        ],
        hide_index=True,
        width="stretch",
    )

    st.markdown("### C. Bench-to-Barn architecture")
    st.markdown(_system_diagram(), unsafe_allow_html=True)

    st.markdown("### D. Wokwi demonstrator")
    st.write(
        "Wokwi demonstrates pin-exact ESP32 integration, firmware execution, sensor input changes, and virtual fault manipulation."
    )
    render_wokwi_status(root)

    st.markdown("### E. Physical Phase 2")
    phase2 = [
        ("Procurement", "PENDING"),
        ("Breadboard", "PENDING"),
        ("Soldering", "PENDING"),
        ("Voltage measurements", "PENDING"),
        ("Physical RS-485", "PENDING"),
        ("SCD41 comparison", "PENDING"),
    ]
    st.dataframe(
        [{"Evidence item": item, "Status": status} for item, status in phase2],
        hide_index=True,
        width="stretch",
    )
    st.markdown(_pcb_concept(), unsafe_allow_html=True)
    st.caption(
        "Prototype carrier PCB concept only; no fabricated PCB or physical solder evidence is claimed."
    )

    st.markdown("### F. Modbus / RS-485")
    left, right = st.columns(2)
    left.metric("Modbus protocol path", "SOFTWARE-TESTED")
    right.metric("Physical RS-485", "PENDING")
    _modbus_summary(root)


def render_wokwi_status(root: Path) -> None:
    """Render only the Wokwi build handoff; the circuit visual appears once above."""
    from dashboard.wokwi_embed import render_wokwi_simulation

    render_wokwi_simulation(compact=True)

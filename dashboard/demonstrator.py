"""Bench-to-barn demonstrator overview for the interview dashboard."""

from pathlib import Path

import streamlit as st

STAGES = [
    ("1", "Farm context", "LVAT-like livestock building and service-area deployment", "Documented"),
    ("2", "Sensor selection", "DHT22 / DS18B20 / BMP180 / SCD41 decision path", "Documented"),
    ("3", "Exact integration", "ESP32 pin map, firmware interfaces and local build", "Implemented"),
    ("4", "Assembly", "Breadboard first, KiCad carrier board as the production path", "Design stage"),
    ("5", "Drivers", "PlatformIO libraries, USB-UART setup, serial and flash workflow", "Documented"),
    ("6", "Commissioning", "Voltage checks, acquisition, faults, Modbus and QA/QC", "Template ready"),
    ("7", "Barn ecosystem", "Local log, RS-485 reference path, MQTT and dashboard", "Implemented"),
]


PIN_ROWS = [
    ("DHT22", "GPIO4", "Digital", "Temperature + RH"),
    ("DS18B20", "GPIO15", "1-Wire", "Redundant temperature"),
    ("BMP180", "GPIO21 / GPIO22", "I2C", "Pressure + temperature"),
    ("MQ-2 surrogate", "GPIO34", "ADC", "Analog acquisition path only"),
    ("microSD", "GPIO5 / 18 / 19 / 23", "SPI", "Local CSV logging"),
    ("RS-485", "GPIO16 / 17 / 27", "UART2", "Modbus reference path"),
]


REQUIREMENTS = [
    ("Sensor integration", "Wokwi diagram + modular ESP32 drivers", "Implemented"),
    ("Interfaces", "Digital, 1-Wire, I2C, SPI, UART/RS-485, WiFi/MQTT", "Implemented / design"),
    ("Data logging", "microSD CSV role + Python local run log", "Implemented"),
    ("Fault detection", "Sensor, network, storage and QA/QC injection", "Implemented"),
    ("Calibration and validation", "Chronological holdout + reference workflow", "Implemented / synthetic"),
    ("Wiring and soldering", "Pin map now; physical evidence required", "Pending evidence"),
    ("Farm commissioning", "Protocol and report templates", "Template ready"),
]


def _status_color(status: str) -> str:
    if status in {"Implemented", "Documented"}:
        return "#147d72"
    if status in {"Design stage", "Template ready", "Implemented / design", "Implemented / synthetic"}:
        return "#ad6b00"
    return "#8a3d3d"


def _sensor_card(name: str, kind: str, interface: str, role: str, state: str) -> str:
    return (
        '<div style="background:#fff;border:1px solid #dce5eb;border-top:4px solid #147d72;'
        'border-radius:8px;padding:14px;min-height:150px">'
        f'<div style="font-size:12px;color:#657b84">{kind}</div>'
        f'<h4 style="margin:5px 0;color:#173f43">{name}</h4>'
        f'<p style="margin:4px 0;font-size:13px"><b>Bus:</b> {interface}</p>'
        f'<p style="margin:4px 0;font-size:13px;color:#345464">{role}</p>'
        f'<strong style="color:#147d72">{state}</strong>'
        "</div>"
    )


def _system_diagram() -> str:
    return """<svg viewBox="0 0 1200 430" role="img" aria-label="Barn sensor node data ecosystem" style="width:100%;background:#f8fbfc;border:1px solid #dce5eb;border-radius:8px">
    <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#147d72"/></marker></defs>
    <style>text{font-family:Arial,sans-serif;fill:#173f43}.label{font-size:15px;font-weight:bold}.small{font-size:12px;fill:#345464}.box{fill:#fff;stroke:#b8ccd2;stroke-width:2}.arrow{stroke:#147d72;stroke-width:3;fill:none;marker-end:url(#arrow)}</style>
    <rect class="box" x="30" y="130" width="180" height="150" rx="10" fill="#e8f3ef"/><text class="label" x="55" y="165">LVAT-like barn</text><text class="small" x="55" y="192">service / exhaust zone</text><text class="small" x="55" y="220">dust · humidity · airflow</text><text class="small" x="55" y="248">deployment context</text>
    <rect class="box" x="275" y="75" width="230" height="260" rx="10"/><text class="label" x="305" y="112">ESP32 sensor node</text><text class="small" x="305" y="143">DHT22 · DS18B20</text><text class="small" x="305" y="166">BMP180 · MQ-2</text><text class="small" x="305" y="189">QA/QC + fault flags</text><text class="small" x="305" y="212">local scheduler</text><text class="small" x="305" y="250">microSD logging</text><text class="small" x="305" y="273">RS-485 / Modbus</text><text class="small" x="305" y="296">WiFi / MQTT</text>
    <rect class="box" x="575" y="40" width="190" height="100" rx="10"/><text class="label" x="605" y="78">Local evidence</text><text class="small" x="605" y="104">CSV · timestamps</text><text class="small" x="605" y="124">quality flags</text>
    <rect class="box" x="575" y="190" width="190" height="100" rx="10"/><text class="label" x="605" y="228">Reference path</text><text class="small" x="605" y="254">RS-485 / Modbus</text><text class="small" x="605" y="274">bench instrument</text>
    <rect class="box" x="865" y="110" width="300" height="190" rx="10"/><text class="label" x="900" y="150">Local digital ecosystem</text><text class="small" x="900" y="180">MQTT / receiver</text><text class="small" x="900" y="204">Streamlit live twin</text><text class="small" x="900" y="228">validation analytics</text><text class="small" x="900" y="252">campaign report</text>
    <path class="arrow" d="M210 205 H275"/><path class="arrow" d="M505 155 H575"/><path class="arrow" d="M505 260 H575"/><path class="arrow" d="M505 300 C690 360 780 315 865 250"/><path class="arrow" d="M765 90 C850 55 875 115 865 145"/>
    </svg>"""


def _pcb_concept() -> str:
    return """<svg viewBox="0 0 900 430" role="img" aria-label="Two layer carrier board concept" style="width:100%;background:#102b2b;border-radius:8px">
    <style>text{font-family:Arial,sans-serif;fill:#eff9f4}.board{fill:#1a6256;stroke:#9dd5b9;stroke-width:3}.part{fill:#d9a441;stroke:#fff0b8;stroke-width:2}.conn{fill:#374b5a;stroke:#b9d0d8;stroke-width:2}.trace{stroke:#e8c46b;stroke-width:4;fill:none}.small{font-size:13px}.title{font-size:20px;font-weight:bold}</style>
    <rect class="board" x="90" y="55" width="720" height="320" rx="12"/><text class="title" x="120" y="90">ESP32 carrier board concept · 2-layer PCB</text>
    <rect class="conn" x="125" y="135" width="120" height="95" rx="5"/><text x="145" y="185">12 V IN</text><text class="small" x="145" y="207">TVS + regulator</text>
    <rect class="part" x="340" y="125" width="180" height="130" rx="8"/><text x="375" y="185">ESP32 DevKit</text><text class="small" x="375" y="207">headers · USB</text>
    <rect class="conn" x="610" y="125" width="145" height="55" rx="5"/><text x="635" y="158">RS-485 A/B</text>
    <rect class="conn" x="610" y="205" width="145" height="55" rx="5"/><text x="644" y="238">SENSOR IO</text>
    <rect class="conn" x="610" y="285" width="145" height="55" rx="5"/><text x="644" y="318">microSD</text>
    <path class="trace" d="M245 182 H340 M520 160 H610 M520 205 H610 M520 235 C570 280 590 315 610 315"/>
    <text class="small" x="125" y="300">Hand solder: headers, terminals, pull-up, LED, RS-485 module</text><text class="small" x="125" y="325">Production path: protection, test points, enclosure connectors</text>
    </svg>"""


def demonstrator_page(root: Path, twin, running: bool) -> None:
    """Render the end-to-end demonstrator narrative and evidence boundaries."""
    st.markdown("### Bench-to-Barn Engineering Demonstrator")
    st.caption(
        "A modular IoT livestock monitoring node, shown from farm context and sensor selection "
        "through embedded integration, commissioning and data flow."
    )
    st.info(
        "The farm context is LVAT-like, not a claim of installation at LVAT. Synthetic data and "
        "design-stage hardware are labelled explicitly; physical evidence is added only after testing."
    )

    st.markdown("#### Live local simulation")
    live_last = twin.records[-1]
    live_cols = st.columns(5)
    live_cols[0].metric("Simulation", "RUNNING" if running else "PAUSED")
    live_cols[1].metric("Samples", len(twin.records))
    live_cols[2].metric("Temperature", f"{live_last['temperature_c']:.1f} °C")
    live_cols[3].metric("Humidity", f"{live_last['relative_humidity_pct']:.1f} %")
    live_cols[4].metric("NH3", f"{live_last['nh3_raw_ppm']:.1f} ppm")
    st.caption("This is the local Python twin. It is live and fault-injectable; it is not a physical ESP32 stream.")
    live_frame = twin.records[-60:]
    st.line_chart(
        {"Temperature °C": [row["temperature_c"] for row in live_frame],
         "Humidity %": [row["relative_humidity_pct"] for row in live_frame]},
        height=220,
    )

    st.markdown("#### Sensors and interfaces")
    sensor_html = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px">'
    sensor_html += _sensor_card("DHT22", "Environmental sensor", "Digital · GPIO4", "Temperature + RH", "Wokwi + firmware")
    sensor_html += _sensor_card("DS18B20", "Redundant temperature", "1-Wire · GPIO15", "Independent temperature check", "Wokwi + firmware")
    sensor_html += _sensor_card("BMP180", "Pressure sensor", "I2C · GPIO21/22", "Pressure + temperature", "Wokwi + firmware")
    sensor_html += _sensor_card("SCD41", "Bench extension", "I2C", "CO2 + temperature + RH comparison", "Bench target")
    sensor_html += _sensor_card("MQ-2", "Gas surrogate", "ADC · GPIO34", "Analog acquisition path only", "Simulation only")
    st.markdown(sensor_html + "</div>", unsafe_allow_html=True)

    visual_tab, wiring_tab, pcb_tab, ecosystem_tab = st.tabs(
        ["Visual node", "Pin-to-pin wiring", "PCB / assembly", "Whole system"]
    )
    with visual_tab:
        st.image(str(root / "docs/figures/virtual_hardware_overview.svg"), width="stretch")
        st.caption("Virtual node layout from the repository Wokwi diagram. It is an integration visual, not electrical validation.")
        st.image(str(root / "docs/figures/prototype_components.svg"), width="stretch")
    with wiring_tab:
        st.image(str(root / "docs/figures/esp32_pin_connections.svg"), width="stretch")
        st.markdown("##### Pin-level contract")
        st.dataframe(
            [{"Component": c, "ESP32 pins": p, "Interface": i, "Role": r} for c, p, i, r in PIN_ROWS],
            hide_index=True,
            width="stretch",
        )
    with pcb_tab:
        st.markdown(_pcb_concept(), unsafe_allow_html=True)
        st.caption("Conceptual carrier board only. No fabricated PCB or physical solder evidence is claimed.")
        st.markdown("**Manual solder points:** ESP32 headers, screw terminals, DS18B20 pull-up, status LED, microSD header and RS-485 module pads.")
    with ecosystem_tab:
        st.markdown(_system_diagram(), unsafe_allow_html=True)
        st.caption("Barn deployment concept: local logging and QA/QC remain available when network transport is unavailable.")

    st.markdown("#### Demonstrator stages")
    stage_html = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px">'
    for number, title, detail, status in STAGES:
        stage_html += (
            '<div style="background:#fff;border:1px solid #dce5eb;border-radius:8px;padding:12px;min-height:130px">'
            f'<div style="font-size:12px;color:#657b84">STAGE {number}</div>'
            f'<h4 style="margin:6px 0;color:#173f43">{title}</h4>'
            f'<p style="font-size:13px;margin:0 0 10px;color:#345464">{detail}</p>'
            f'<strong style="color:{_status_color(status)}">{status}</strong>'
            "</div>"
        )
    st.markdown(stage_html + "</div>", unsafe_allow_html=True)

    st.markdown("#### Barn-to-dashboard data flow")
    st.code(
        "LVAT-like barn / service area\n"
        "  -> ESP32 sensor node\n"
        "     -> local QA/QC and fault flags\n"
        "     -> microSD CSV log\n"
        "     -> RS-485 / Modbus reference path (bench)\n"
        "     -> WiFi / MQTT (optional transport)\n"
        "        -> local receiver / database\n"
        "           -> Streamlit dashboard and validation reports",
        language="text",
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### Exact integration contract")
        st.dataframe(
            [{"Component": c, "ESP32 pins": p, "Interface": i, "Role": r} for c, p, i, r in PIN_ROWS],
            hide_index=True,
            width="stretch",
        )
    with right:
        st.markdown("#### Requirement coverage")
        st.dataframe(
            [{"Requirement": r, "Evidence": e, "Status": s} for r, e, s in REQUIREMENTS],
            hide_index=True,
            width="stretch",
        )

    with st.expander("Why the hybrid simulation strategy?", expanded=False):
        st.markdown(
            "Wokwi is retained for visible ESP32 wiring and firmware integration. It does not "
            "prove humidity benchmarking, analogue NH3 selectivity, soldering, RS-485 electrical "
            "behaviour or host-driver installation. Those claims belong to the bench layer. "
            "The local Python twin remains the repeatable QA/QC and fault-injection environment."
        )

    with st.expander("Evidence still required", expanded=False):
        st.markdown(
            "- Real component procurement record\n"
            "- Breadboard or perfboard assembly photos\n"
            "- Measured supply rails and continuity checks\n"
            "- USB-UART driver and flashing record\n"
            "- DHT22 versus SCD41 bench comparison\n"
            "- Physical RS-485 test and completed commissioning report"
        )

    st.markdown("#### Repository map")
    st.markdown(
        "[Farm context](../docs/02_farm_context.md) · "
        "[Sensor selection](../docs/03_sensor_selection.md) · "
        "[Driver configuration](../docs/06_driver_configuration.md) · "
        "[Physical bench plan](../docs/09_physical_bench_plan.md) · "
        "[Commissioning](../docs/07_commissioning.md) · "
        "[System architecture](../docs/04_system_architecture.md)"
    )

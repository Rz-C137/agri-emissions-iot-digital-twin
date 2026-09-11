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


def demonstrator_page(root: Path) -> None:
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
        "[Farm context](../docs/farm_context.md) · "
        "[Sensor procurement](../docs/sensor_procurement.md) · "
        "[Driver configuration](../docs/driver_configuration.md) · "
        "[PCB concept](../docs/pcb_design.md) · "
        "[Commissioning report](../docs/bench_commissioning_report.md) · "
        "[Ecosystem overview](../docs/ecosystem_overview.md)"
    )

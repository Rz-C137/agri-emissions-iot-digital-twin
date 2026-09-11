"""Multi-temperature sensor commissioning panel (mirrors firmware TEMP_QC)."""

import streamlit as st

from simulator.sensor_validation import (
    DEFAULT_THRESHOLD_C,
    TEMP_FAULT_MODES,
    assess_temperature_agreement,
)


def _status_badge(status: str) -> str:
    if status == "PASS":
        return "✅ OK"
    if status == "WARNING":
        return "⚠️ WARNING"
    return "❌ " + status


def sensor_commissioning_page(twin) -> None:
    st.markdown("### 🌡️ Sensor Commissioning — Temperature Redundancy")
    st.caption(
        "Three independent temperature paths (DHT22, DS18B20, BMP180) are compared each sample. "
        "Inject a fault to demonstrate `TEMP_SENSOR_DISAGREEMENT` handling."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        fault = st.selectbox(
            "Temperature fault injection", TEMP_FAULT_MODES, key="ui_temp_fault_mode"
        )
        current_fault = getattr(twin, "temp_fault_mode", "NONE")
        if fault != current_fault and hasattr(twin, "set_temp_fault"):
            twin.set_temp_fault(fault)
    with col_b:
        threshold = st.number_input(
            "Acceptance threshold (°C)",
            min_value=0.1,
            max_value=5.0,
            value=DEFAULT_THRESHOLD_C,
            step=0.1,
        )

    if st.button("Advance one sample", key="temp_qc_step"):
        twin.step(1)
        st.rerun()

    if not twin.records:
        st.info("Advance the twin to populate commissioning readings.")
        return

    last = twin.records[-1]
    qc = assess_temperature_agreement(
        last.get("temperature_dht22_c"),
        last.get("temperature_ds18b20_c"),
        last.get("temperature_bmp180_c"),
        threshold_c=threshold,
    )

    rows = []
    for name, key in (
        ("DHT22", "temperature_dht22_c"),
        ("DS18B20", "temperature_ds18b20_c"),
        ("BMP180", "temperature_bmp180_c"),
    ):
        value = last.get(key)
        reading = f"{value:.1f} °C" if value is not None else "—"
        sensor_status = "OK" if value is not None else "MISSING"
        if qc["status"] == "WARNING" and qc["suspected_sensor"] == name:
            sensor_status = "SUSPECT"
        rows.append({"Sensor": name, "Reading": reading, "Status": sensor_status})

    st.dataframe(rows, hide_index=True, width="stretch")

    max_delta = qc["max_disagreement_c"]
    st.markdown(
        f"**Maximum disagreement:** {max_delta:.1f} °C  \n"
        f"**Acceptance threshold:** {threshold:.1f} °C  \n"
        f"**Overall status:** {_status_badge(qc['status'])}"
    )
    if qc["status"] == "WARNING":
        st.warning(f"Suspected sensor: **{qc['suspected_sensor']}**  \nFlag: `{qc['flag']}`")
    elif qc["status"] == "PASS":
        st.success("All temperature channels agree within threshold.")

    st.markdown("#### Recent disagreement trend")
    import pandas as pd

    frame = pd.DataFrame(twin.records[-30:])
    if "temp_max_disagreement_c" in frame.columns:
        st.line_chart(frame.set_index("timestamp")["temp_max_disagreement_c"])
    st.caption(
        "Wokwi/firmware serial line: `# TEMP_QC,dht=...,ds18=...,bmp=...,max_delta=...,status=...,suspect=...`"
    )

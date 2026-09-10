"""Offline interview dashboard for a virtual measurement system."""

import sys
from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dashboard.commissioning import commissioning_page  # noqa: E402
from dashboard.hardware import glance, hardware_page  # noqa: E402
from simulator.engine import SENSOR_MODES, Twin  # noqa: E402
from simulator.health import assess  # noqa: E402
from simulator.model import Config  # noqa: E402
from validation.analysis import calibrate, dataset  # noqa: E402

st.set_page_config(page_title="Agri Emissions | Virtual Commissioning", layout="wide")
st.markdown(
    """<style>
.stApp {background:#f5f7f9;color:#18303b}
[data-testid="stMetric"] {background:white;border:1px solid #dde5e9;
border-radius:8px;padding:16px}
h1,h2,h3 {color:#173f43} .block-container {padding-top:4rem}
</style>""",
    unsafe_allow_html=True,
)

if "twin" not in st.session_state:
    st.session_state.twin = Twin(log_path=ROOT / "data/runs" / f"{uuid4().hex}.csv")
    st.session_state.twin.step(120)
twin = st.session_state.twin

with st.sidebar:
    st.markdown("### AGRI EMISSIONS\nVirtual Commissioning Prototype")
    st.caption("VIRTUAL SYSTEM · SIMULATED DATA")
    page = st.radio(
        "Navigation",
        [
            "🏠 Overview & Live System",
            "🔧 Hardware & Architecture", 
            "📊 Validation & Technical Details",
        ],
    )
    st.divider()
    running = st.toggle("Run simulation", value=False)
    if st.button("Advance 10 samples", width="stretch"):
        twin.step(10)
    interval = st.selectbox("Sampling interval (seconds)", [60, 10, 300])
    if st.button("Reset deterministic session", width="stretch"):
        st.session_state.twin = Twin(
            Config(interval_s=interval), ROOT / "data/runs" / f"{uuid4().hex}.csv"
        )
        st.session_state.twin.step(120)
        st.rerun()
    st.caption("Run advances one simulated sample per second. Sampling interval applies on reset.")


def line(frame: pd.DataFrame, columns: list[str], title: str, unit: str) -> None:
    fig = px.line(
        frame,
        x="timestamp",
        y=columns,
        title=title,
        labels={"value": unit, "timestamp": "Simulated time (UTC)", "variable": "Signal"},
        color_discrete_sequence=["#127f80", "#e29836", "#7c68ad"],
    )
    fig.update_layout(legend_title_text="", margin=dict(l=10, r=10, t=45, b=10), height=330)
    names = {
        "nh3_raw_ppm": "Raw sensor",
        "nh3_reference_ppm": "Virtual reference",
        "nh3_calibrated_ppm": "Calibrated sensor",
        "temperature_c": "Temperature",
        "relative_humidity_pct": "Relative humidity",
        "co2_ppm": "Synthetic CO₂",
    }
    fig.for_each_trace(lambda trace: trace.update(name=names.get(trace.name, trace.name)))
    st.plotly_chart(fig, width="stretch")


@st.cache_data
def validation_data() -> tuple[pd.DataFrame, dict]:
    return calibrate(dataset())


@st.fragment(run_every=1 if running else None)
def content() -> None:
    if running:
        twin.step()
    frame = pd.DataFrame(twin.records)
    last = twin.records[-1]
    available = np.isfinite(frame.nh3_raw_ppm)
    completeness = 100 * available.mean()
    st.caption("SYNTHETIC MEASUREMENTS · NO PHYSICAL FARM DATA")

    page_title = page.split(" ", 1)[1] if " " in page else page
    st.title(page_title)

    if page == "🏠 Overview & Live System":
        st.markdown(
            "**Virtual commissioning prototype demonstrating firmware architecture, fault handling, and data quality assurance**"
        )
        st.info(
            "⚠️ **Virtual system with simulated sensors.** Physical integration, lab calibration, and field deployment are future stages."
        )
        
        # Fault Injection Controls
        with st.expander("🔧 Fault Injection & System Controls", expanded=False):
            st.caption("Inject faults independently to test system resilience")
            environment, sensor, infrastructure = st.columns(3)
            with environment:
                st.markdown("**Synthetic environment**")
                if st.button("Increase synthetic NH₃"):
                    twin.set_environment("HIGH_NH3")
                    twin.step()
                    st.rerun()
                if st.button("Baseline environment"):
                    twin.set_environment("NORMAL")
                    twin.step()
                    st.rerun()
            with sensor:
                st.markdown("**Gas acquisition**")
                mode = st.selectbox("Gas fault", SENSOR_MODES[1:])
                if st.button("Apply gas fault"):
                    twin.set_sensor(mode)
                    twin.step()
                    st.rerun()
                if st.button("Restore sensor"):
                    twin.set_sensor("NORMAL")
                    twin.step()
                    st.rerun()
            with infrastructure:
                st.markdown("**Infrastructure**")
                for label, action, target in [
                    ("Disconnect network", twin.set_network, False),
                    ("Restore network only", twin.set_network, True),
                    ("Fail storage", twin.set_storage, False),
                    ("Restore storage only", twin.set_storage, True),
                ]:
                    if st.button(label):
                        action(target)
                        twin.step()
                        st.rerun()
            if st.button("Restore all faults"):
                twin.restore_all()
                twin.step()
                st.rerun()
            st.caption("Restore all faults leaves environment unchanged")
        
        # System Health Status
        health = assess(last, twin.network, twin.storage)
        if health.measurement_system == "OPERATIONAL":
            st.success(
                "Measurement system operational · acquisition, local logging and simulated delivery active"
            )
        else:
            st.warning(f"Measurement system: {health.measurement_system.replace('_', ' ').lower()}")
        st.markdown(
            f"**Environmental indication:** {health.environmental_condition} · "
            f"**Data quality:** {health.data_quality}"
        )
        if twin.network == "OFFLINE":
            st.info(
                "Measurements continue locally while the network is unavailable. Records await simulated synchronization."
            )
        if twin.storage != "OK":
            st.error(
                "Local storage is unavailable. Pending writes are held in session memory and are at risk if the process stops."
            )
        if last["quality_flags"] != "VALID":
            st.warning(
                f"Current sample requires review: {last['quality_flags']}. Raw values remain available under Data Quality."
            )
        if health.environmental_condition == "ELEVATED":
            st.warning(
                "Elevated synthetic NH₃ signal. The 25 ppm display threshold is an illustrative scenario setting, not an exposure limit."
            )
        a, b, c, d = st.columns(4)
        finite_now = last["nh3_raw_ppm"] is not None and np.isfinite(last["nh3_raw_ppm"])
        a.metric(
            "NH₃ · simulated raw", f"{last['nh3_raw_ppm']:.1f} ppm" if finite_now else "Unavailable"
        )
        b.metric("Air temperature", f"{last['temperature_c']:.1f} °C")
        c.metric("Relative humidity", f"{last['relative_humidity_pct']:.1f} %")
        d.metric("Data completeness", f"{completeness:.1f} %")
        st.markdown(
            f"**Environment:** {twin.environment_mode} · **Gas:** {last['gas_channel_status']} · "
            f"**Network:** {twin.network} · **Storage:** {twin.storage}"
        )
        
        # System at a Glance
        glance(twin, running)
        
        # Live Monitoring Charts
        st.markdown("### 📈 Live Monitoring")
        line(
            frame.tail(180),
            ["nh3_raw_ppm", "nh3_reference_ppm"],
            "NH₃ signal and virtual reference · raw data, including flagged samples",
            "NH₃ (ppm)",
        )
        a, b, c, d = st.columns(4)
        a.metric("Acquisition attempts", len(frame))
        b.metric("Pending telemetry", len(twin.pending))
        c.metric("Simulated receiver records", len(twin.delivered))
        d.metric("Pending local writes", len(twin.local_pending))
        st.caption(
            f"Local log: {len(twin.local_ids)} · Retries: {twin.retries} · "
            f"Recovery time: {twin.recovery_time_s if twin.recovery_time_s is not None else '—'} s"
        )
        
        # Additional environmental charts
        col1, col2 = st.columns(2)
        with col1:
            line(frame.tail(180), ["temperature_c"], "Temperature", "°C")
        with col2:
            line(frame.tail(180), ["relative_humidity_pct"], "Humidity", "%")

    elif page == "🔧 Hardware & Architecture":
        st.markdown(
            "**Virtual hardware demonstration and system architecture**"
        )
        
        # Wokwi simulation (open in browser — Wokwi does not support reliable iframe embed)
        st.markdown("### 🖥️ Virtual Hardware Prototype (Wokwi)")
        st.info(
            "Open the Wokwi browser simulator with this repository's `wokwi/diagram.json` and `wokwi/sketch.ino`. "
            "The circuit shows ESP32 + DHT22 + analog gas surrogate + microSD + status LED."
        )
        st.markdown(
            "[**Open Wokwi ESP32 project**](https://wokwi.com/projects/new/esp32) · "
            "[**Wokwi quick-start guide**](WOKWI_QUICK_START.md) · "
            "[**Pin diagram (SVG)**](docs/figures/esp32_pin_connections.svg)"
        )
        st.image(str(ROOT / "docs/figures/virtual_hardware_overview.svg"), width="stretch")
        st.caption(
            "Repository-owned wiring diagram (checked against `firmware/include/Config.h`). "
            "Physical implementation requires NH₃-B1 with potentiostatic front-end, I²C environmental sensor, and RS-485 Modbus."
        )
        
        # Hardware Details
        with st.expander("📐 Hardware Specifications", expanded=False):
            hardware_page(ROOT)
        
        # System Architecture
        st.markdown("### 🏗️ System Architecture")
        st.info(
            "**Implemented:** ESP32 firmware (DHT22 + ADC + SD), Modbus protocol (host-tested), Python simulation. "
            "**Future:** Physical sensor integration, RS-485 electrical commissioning."
        )
        stages = [
            "Livestock environment\nSynthetic conditions",
            "Virtual sensors\nGas + T/RH",
            "Interfaces / ESP32\nADC + digital acquisition",
            "QA/QC\nRaw values + flags",
            "Local storage / MQTT\nLogging + retry queue",
            "Digital twin\nState + events",
            "Calibration / validation\nIndependent holdout",
        ]
        fig = go.Figure()
        for i, label in enumerate(stages):
            fig.add_annotation(
                x=0.5,
                y=6 - i,
                text=label.replace("\n", "<br>"),
                showarrow=False,
                bgcolor="#e0f0ec",
                borderpad=12,
                font=dict(size=15),
            )
            if i < 6:
                fig.add_annotation(
                    x=0.5,
                    y=5.4 - i,
                    ax=0.5,
                    ay=5.65 - i,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    text="",
                    showarrow=True,
                    arrowhead=2,
                )
        fig.update_layout(
            height=760,
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[-0.6, 6.6]),
            margin=dict(t=0, b=0),
        )
        st.plotly_chart(fig, width="stretch")
        
        # Modbus Commissioning Bench
        with st.expander("🔌 Modbus RTU Commissioning Bench", expanded=False):
            st.markdown("Protocol-level simulation for reference analyzer integration")
            commissioning_page(ROOT)

    elif page == "📊 Validation & Technical Details":
        st.markdown("**Calibration methodology, data quality, and system technical specifications**")
        
        # Calibration & Validation
        st.markdown("### 📐 Calibration & Validation Workflow")
        calibrated, report = validation_data()
        st.write(
            "Current demonstration: affine sensor-to-reference calibration. Temperature/humidity compensation is a possible future extension, not fitted here. A separate, fixed three-day synthetic dataset keeps this comparison reproducible. The first 60% trains a two-parameter linear correction; the final 40% evaluates it without refitting."
        )
        st.caption(
            f"Calibration: corrected = {report['slope']:.4f} × raw + {report['intercept']:.4f} ppm. Training pairs: {report['fit_pairs']}; holdout rows: {report['validation_rows']}."
        )
        st.dataframe(
            pd.DataFrame({"Raw": report["raw"], "Calibrated": report["calibrated"]}),
            width="stretch",
        )
        st.write(
            "Bias is average signed disagreement. MAE is average absolute disagreement. RMSE describes typical disagreement while giving larger errors more weight; lower is better. R² compares errors with reference variability and may be negative. Missing percentage uses all scheduled holdout rows."
        )
        v = calibrated[calibrated.split == "Validation"].copy()
        v["Residual (ppm)"] = v.nh3_calibrated_ppm - v.nh3_reference_ppm
        v["Pair mean (ppm)"] = (v.nh3_calibrated_ppm + v.nh3_reference_ppm) / 2
        agreement = px.scatter(
            v,
            x="Pair mean (ppm)",
            y="Residual (ppm)",
            title="Bland–Altman: descriptive holdout agreement",
        )
        bias, spread = v["Residual (ppm)"].mean(), v["Residual (ppm)"].std()
        for level in (bias, bias - 1.96 * spread, bias + 1.96 * spread):
            agreement.add_hline(y=level, line_dash="dash")
        st.plotly_chart(agreement, width="stretch")
        st.caption(
            "Mean difference ± 1.96 sample SD. Descriptive limits, not confidence intervals or acceptance criteria; time dependence and reference uncertainty remain."
        )
        line(
            v,
            ["nh3_raw_ppm", "nh3_calibrated_ppm", "nh3_reference_ppm"],
            "Independent holdout comparison",
            "NH₃ (ppm)",
        )
        fig = px.scatter(
            v,
            x="nh3_reference_ppm",
            y=["nh3_raw_ppm", "nh3_calibrated_ppm"],
            labels={"nh3_reference_ppm": "Virtual reference (ppm)", "value": "Sensor (ppm)"},
            title="Reference vs sensor",
        )
        low, high = v.nh3_reference_ppm.min(), v.nh3_reference_ppm.max()
        fig.add_scatter(x=[low, high], y=[low, high], mode="lines", name="1:1 agreement")
        st.plotly_chart(fig, width="stretch")
        for x, label in [
            ("nh3_reference_ppm", "Virtual reference (ppm)"),
            ("timestamp", "Time (UTC)"),
            ("temperature_c", "Temperature (°C)"),
            ("relative_humidity_pct", "Relative humidity (%)"),
        ]:
            fig = px.scatter(
                v, x=x, y="Residual (ppm)", labels={x: label}, title=f"Calibrated error vs {label}"
            )
            fig.add_hline(y=0, line_dash="dash")
            st.plotly_chart(fig, width="stretch")
        st.warning(
            "⚠️ **Synthetic validation workflow demonstration.** Not evidence of physical sensor performance. "
            "Laboratory validation with certified reference gases required."
        )
        
        # Data Quality Summary
        st.markdown("### 📋 Data Quality Summary")
        qa, qb, qc = st.columns(3)
        qa.metric("Valid", int((frame.quality_flags == "VALID").sum()))
        qb.metric("Flagged", int((frame.quality_flags != "VALID").sum()))
        qc.metric("Completeness", f"{completeness:.1f}%")
        
        with st.expander("📊 Quality Details & Data Export", expanded=False):
            st.write("Flagged values are retained; no automatic deletion.")
            twin.quality = type(twin.quality)(
                stale_s=2 * twin.config.interval_s,
                outlier_enabled=st.checkbox(
                    "Enable outlier detection", value=twin.quality.outlier_enabled
                ),
            )
            st.dataframe(frame.tail(100), hide_index=True)
            st.download_button(
                "Download CSV",
                frame.to_csv(index=False),
                "measurements.csv",
                "text/csv",
            )
        
        # Event Log
        with st.expander("📜 System Event Log", expanded=False):
            events = pd.DataFrame(twin.events, columns=["timestamp", "severity", "event_type", "description"])
            st.dataframe(events.iloc[::-1].head(50), hide_index=True, width="stretch")
        
        # Technical Details
        st.markdown("### ⚙️ Technical Specifications")
        st.json(
            {
                "sampling_interval_s": twin.config.interval_s,
                "seed": twin.config.seed,
                "interfaces_implemented": "DHT22 digital / ADC analog / microSD SPI (firmware)",
                "interfaces_proposed": "NH₃-B1 electrochemical (requires potentiostat) / SCD41 I²C (driver not coded)",
                "transport": "In-process acknowledged simulation; optional MQTT publisher (QoS 0) is separate",
                "queue": "Session-memory dictionaries keyed by sequence; no silent eviction",
                "storage": str(twin.log_path),
                "quality_contract": "quality_code bitmask + quality_flags pipe-separated names; VALID = 0",
                "time_contract": "timestamp UTC or null; timestamp_status identifies SIMULATED_UTC/NTP_UTC/UNSYNCHRONIZED; uptime_ms is separate",
                "firmware_diagnostics": "Environmental sensor OK/ERROR; analog gas channel UNVERIFIED even with plausible ADC counts",
                "sensor_model": vars(twin.config) | {"start": twin.config.start.isoformat()},
            }
        )
        st.write(
            "**Sensor simulation details:** The gas_raw field in Python is an illustrative 100 counts/ppm signal, not an actual MQ-2 transfer function. "
            "ESP32 firmware (separate implementation) reports simulated ADC counts and leaves NH₃ concentration fields empty. "
            "Calibration in this dashboard is performed only on the independent validation page using a fixed synthetic dataset."
        )
        st.write(
            "**Data persistence:** Memory queues do not survive process termination. CSV files preserve local acquisitions but are not replayed automatically. "
            "Firmware uses a bounded queue and explicitly counts overflows. "
            "**Important:** No emission mass flux can be inferred without validated ventilation measurements and reference-method validation."
        )
        st.write(
            "**Scope boundaries:** This is a virtual commissioning environment for measurement-system architecture and fault-handling logic. "
            "It does **not** simulate barn physics, airflow, animal physiology, or manure processes. "
            "See `docs/validation_protocol.md` and `docs/marvela_alignment.md` for the proposed physical validation pathway."
        )


content()

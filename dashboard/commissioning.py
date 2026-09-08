"""Interactive, offline protocol bench for the separate commissioning campaign."""

import pandas as pd
import streamlit as st

from simulator.campaign import acquire, run_campaign


def commissioning_page(root):
    st.write("Industrial interface bench · synthetic NH₃ / CH₄ / N₂O")
    st.caption(
        "Independent Python byte-level Modbus RTU emulator. No serial port, physical RS-485 bus or live ESP32 connection."
    )
    site = st.selectbox("Virtual campaign context", ["barn", "manure"])
    fault = st.selectbox("Reference communication", ["OK", "TIMEOUT", "BAD_CRC"])
    sequence = st.slider("Synthetic sample index", 0, 119, 10)
    record = acquire(sequence, site=site, fault=fault)
    st.code(f"TX  {record['request_hex']}\nRX  {record['response_hex'] or '(no response)'}")
    if record["reference_status"] == "VALID":
        st.success("CRC, unit address, function and response length verified")
    else:
        st.error(record["reference_status"] + " · reference values remain missing")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Gas": gas.upper(),
                    "Raw ppm": record[f"{gas}_raw_ppm"],
                    "Virtual reference ppm": record[f"{gas}_reference_ppm"],
                }
                for gas in ("nh3", "ch4", "n2o")
            ]
        ),
        hide_index=True,
    )
    st.markdown(
        "**Local recovery experiment:** 120 acquisition attempts, 60-sample network outage, five reference timeouts and five corrupted responses. A SQLite spool and idempotent local receiver retain raw records, including missing references."
    )
    if st.button("Run reproducible commissioning campaign"):
        summary = run_campaign(root / "data/runs" / f"commissioning-{site}", site=site)
        st.json(summary)
    st.info(
        "SQLite persistence belongs to this separate commissioning bench. The original live twin and firmware still have volatile queues. Electrical noise, timing, flash endurance and power loss are not physically modeled."
    )
    st.markdown(
        "See [the laboratory-to-farm workflow](https://github.com/Rz-C137/agri-emissions-iot-digital-twin/blob/main/docs/marvela_alignment.md) for wiring, acceptance gates and the job-requirement mapping."
    )

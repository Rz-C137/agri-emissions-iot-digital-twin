# Interview demonstration

Start Streamlit, select Fault Injection and leave automatic running off for precise pacing. Each button changes one dimension and advances one sample. Infrastructure and sensor restoration never resets the synthetic environment. All values and the reference are virtual.

## 90-second demonstration

| Time | Action and first-person explanation |
| --- | --- |
| 0–15 s | Overview: I model the measurement system, not full barn physics. I separate environmental indication from acquisition, communications, storage and data quality. |
| 15–35 s | Fault Injection → Disconnect network → Advance 10 samples. I keep acquisition independent of network availability because a telemetry outage should not interrupt local measurements. The pending queue grows while local records continue. |
| 35–50 s | Restore network only. I reconcile the pending records in this controlled simulation; I am not claiming reboot-safe delivery. |
| 50–70 s | Apply gas fault (SENSOR_DISCONNECTED), then Restore sensor. I preserve the acquisition attempt and attach quality information rather than silently deleting an abnormal observation. Ambient measurements continue. |
| 70–90 s | Calibration & Validation. I fit an affine correction on earlier samples and evaluate later ones. I treat the virtual reference as a lower-error comparison instrument, not absolute ground truth. |

## 5-minute technical demonstration

| Time | Action and first-person explanation |
| --- | --- |
| 0:00–0:30 | Overview, normal monitoring. I show synthetic NH₃, °C and RH alongside six distinct health dimensions. None of this is a farm campaign. |
| 0:30–0:55 | Increase synthetic NH₃. I demonstrate an elevated condition without equating it to broken acquisition. Abrupt-change flags remain visible and raw data is retained. |
| 0:55–1:30 | Disconnect network; advance ten samples. I show local records, total attempts and pending telemetry separately. The elevated environment remains active. |
| 1:30–1:50 | Restore network only. I show synchronized receiver counts and the timestamped recovery event. Queued telemetry remains volatile until serviced. |
| 1:50–2:20 | Fail storage; advance ten samples. I show the failed local-write path while the network remains online. Restore storage only and show pending local writes backfilled. |
| 2:20–2:55 | Apply gas fault, then Data Quality. I preserve the raw observation/failed attempt and quality_code plus readable quality_flags. DHT diagnostics and analog gas-channel health are different: a plausible ADC voltage does not prove a real gas sensor is healthy. |
| 2:55–3:15 | Restore sensor. I restore only acquisition; the synthetic environment remains elevated until I choose Baseline environment. |
| 3:15–4:15 | Calibration & Validation. I retain the chronological holdout and explain bias/RMSE and residuals. Temperature/humidity compensation is a possible future extension, not the model fitted here. |
| 4:15–5:00 | Technical Details / firmware. I distinguish simulated UTC, NTP-derived time and uptime. Firmware rejects new telemetry on queue overflow and reports it; QoS 0 does not acknowledge end-to-end delivery. I would validate a conditioned analog front end and a suitable NH₃ instrument against a traceable reference before physical claims. |

For an additional combined-fault challenge, disconnect the network, fail storage and apply a gas fault. Restore network only and verify storage and sensor faults remain. Restore storage only while the network is offline to demonstrate the opposite direction. **Restore all faults** is an explicit convenience, never an implicit recovery side effect.

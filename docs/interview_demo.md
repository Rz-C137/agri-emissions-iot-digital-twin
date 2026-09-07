# Interview demonstration

Before the interview, install dependencies, start Streamlit and open Overview. Keep the internet disconnected if desired. The primary demo needs no accounts. Open a terminal at the repository for optional code inspection. Use manual steps for reliable timing and reset to start fresh.

## Five-minute sequence

| Time | Action | Suggested first-person explanation |
| --- | --- | --- |
| 0:00–0:35 | Overview | I built a virtual measurement-system twin to examine how sensor readings become trustworthy records. Every value here is synthetic; I am demonstrating concentration monitoring, not measured farm emissions. |
| 0:35–1:00 | Live Monitoring; advance ten samples | I keep acquisition, sensor state and communication state visible separately. Temperature, humidity and the gas signal evolve with simulated time. |
| 1:00–1:25 | Fault Injection → HIGH_NH3 → Apply | I inject an elevated concentration. The signal changes and the quality layer flags the abrupt transition for review; it does not delete it. |
| 1:25–2:05 | NETWORK_OFFLINE → Apply; advance ten samples | I continue collecting and logging while the network is unavailable. Compare total attempts, local records and pending telemetry. |
| 2:05–2:30 | RECOVERY → Apply | I restore the simulated link. Pending records are acknowledged and the receiver count catches up. This proves record accounting within this session, not physical-network durability. |
| 2:30–3:05 | SENSOR_DISCONNECTED → Apply | I fail the gas acquisition while ambient sensing continues. A missing value cannot appear as a valid NH₃ measurement. Retries and events are visible. |
| 3:05–3:30 | Data Quality | I retain every attempt, count missing data separately from flagged finite readings and preserve raw evidence for review. |
| 3:30–4:25 | Calibration & Validation | I fit a simple linear correction on earlier synthetic data and evaluate later samples. RMSE summarizes disagreement; residual plots show where the model remains imperfect. This reference is also virtual. |
| 4:25–5:00 | Architecture / Technical Details | I separated hardware APIs from logic. The next step would be an NH₃-appropriate instrument, reference traceability, controlled environmental testing and power-safe delivery. MQ2 only demonstrates ADC acquisition. |

## 90-second sequence

1. **0–15 seconds:** Overview: synthetic concentration, system health, independent portfolio scope.
2. **15–40 seconds:** Inject NETWORK_OFFLINE, advance ten samples, show local and pending counts.
3. **40–55 seconds:** Apply RECOVERY; show receiver catch-up and synchronization event.
4. **55–70 seconds:** Apply SENSOR_DISCONNECTED; show missing gas value and quality flag.
5. **70–90 seconds:** Calibration page: chronological holdout and residuals; explain the proposed physical validation pathway.

## Questions I am prepared to answer

- **Does it measure NH₃ with MQ2?** No. The NH₃ instrument is synthetic Python data. ESP32 MQ2 readings remain analog surrogate counts.
- **Does no data loss survive power failure?** No. The demonstrated no-gap invariant covers the running Python session. Durable replay and physical fault tests are future work.
- **Why a simple calibration?** Its slope/intercept and residual structure are explainable; better synthetic metrics alone would not justify a more complex model.
- **Why call it a digital twin?** It mirrors a measurement system's acquisition, quality and operational states. It is not a full building model.

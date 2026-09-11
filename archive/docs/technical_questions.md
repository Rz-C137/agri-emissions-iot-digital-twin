# Technical discussion prompts

| Question | My answer and demonstration boundary |
| --- | --- |
| Why RS-485 and Modbus? | Differential signaling and device addressing suit industrial integration. RS-485 needs a transceiver; Modbus supplies a protocol. I test bytes, not a farm cable. |
| Why not call DHT22 I²C? | It uses its own digital single-wire protocol. I²C21/22 is only reserved in this design. |
| Why ADC1 GPIO34? | It is an input-capable ADC1 path on this ESP32 setup; counts need conditioning and calibration and cannot prove gas selectivity. |
| What does CRC establish? | Frame integrity against many accidental errors, not authenticity, freshness, correct units or sensor accuracy. |
| What happens on a reference timeout? | The attempted acquisition is retained with missing reference values and a reason; no stale value is silently reused. |
| Does MQTT guarantee no duplicates? | No. The current firmware uses QoS0. Durable identity and receiver deduplication are separate concerns; the new local bench tests lost-ack retry. |
| What survives a restart? | Committed records in the new SQLite campaign spool. Original Python and firmware queues are volatile; uncommitted samples and physical power loss remain separate issues. |
| Is calibrated agreement traceable? | Not here. Real traceability requires documented standards, certificates and an uncertainty chain. The synthetic artifact records reproducibility provenance only. |
| Why hold out time? | Nearby samples share structure. A later block reduces leakage, but independent devices/days/sites would be stronger physical validation. |
| Is a Bland–Altman band a confidence interval? | No. These are descriptive mean difference ± 1.96 sample SD limits; repeated, correlated observations and heteroscedasticity require further analysis. |
| Is concentration an emission rate? | No. Flow/ventilation or a justified flux method, background correction, units and uncertainty are also needed. |
| How would I diagnose noisy measurements? | Separate reference status, raw signal, environment, power/grounding, sampling line, timing and communications; perturb one cause at a time and preserve evidence. |
| How would I coordinate a campaign? | Agree requirements and owners, freeze interfaces, document deviations, review quality and uncertainty, and hand over reproducible records. This is my proposed workflow, not claimed prior partner work. |

# Limitations

- Every measurement is simulated. No physical experiments, farm campaign, hardware tests, certified procedure or organizational affiliation are claimed.
- The twin represents measurement-system state. It does not simulate complete barn physics, CFD, airflow, animal physiology or manure processes.
- NH₃ concentration alone is not an emission rate. Ventilation, representative sampling and uncertainty propagation are absent.
- MQ2 is a cross-sensitive combustible-gas surrogate, not a selective NH₃ instrument. No MQ2-to-NH₃ conversion is implemented.
- Synthetic distributions and sensor coefficients are assumptions, not empirical estimates. Virtual agreement cannot establish selectivity, traceability, detection limit or field accuracy.
- Calibration shares the synthetic environment with the virtual reference. A chronological holdout prevents direct fitting leakage but does not establish transfer to new buildings, sensor units or instruments.
- The Python application does not ingest live ESP32 or broker records. Its network state refers to an in-process transport simulation.
- Dashboard queues and events are session memory. Local CSV survives process exit, but automatic restart replay is not implemented. Long sessions consume increasing memory and are intended for short demonstrations.
- A combined process/power failure during an unlogged outage can lose volatile records. Filesystem writes do not claim power-fail atomicity or disk-controller durability.
- Firmware has 120 volatile telemetry slots, explicit overflow counters and no SD replay. Failed local writes are reported but not backfilled after SD recovery. MQTT QoS 0 can lose accepted transmissions; no end-to-end no-loss claim applies to firmware.
- The optional Python publisher uses QoS 1 and checkpointing. Duplicate publication remains possible after interruption, and broker acknowledgement does not prove every downstream database action succeeded.
- DHT acquisition and MQTT connection calls can block briefly. The firmware is cooperative, not hard real-time. Analog pin floating/saturation cannot reliably diagnose every MQ2 wiring fault.
- NTP-unavailable firmware UTC is null/blank with UNSYNCHRONIZED status; uptime is a separate duration. Restarted sequence numbers require a run identifier in a future multi-session ingestion bridge.
- Wokwi does not validate physical voltage safety, contamination resistance, sensor warm-up, component aging or EMC. A real MQ2 module may require output conditioning before a 3.3 V ESP32 ADC.
- The current diagrams, browser setup and firmware compilation support reproducibility; the revision-specific browser and physical verification evidence is recorded separately in verification.md.

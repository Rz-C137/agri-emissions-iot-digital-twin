# Measurement contract

The Python twin and the ESP32/Wokwi application are separate producers. Streamlit does not ingest live firmware. Shared field names and meanings support review and a future adapter; they are not evidence of an implemented bridge.

## Quality

`quality_code` is an integer bitmask. `quality_flags` is a human-readable **pipe-separated string**, used consistently in Python records, CSV, firmware JSON and ThingsBoard scalar telemetry. Flag order has no meaning. Zero is `VALID`; a nonzero code includes each active name once. VALID means no implemented check failed, not a calibrated or proven-healthy instrument.

| Bit | Name | Meaning |
| --- | --- | --- |
| 1 | MISSING | Required acquired value absent; includes DHT driver's failed-read NaN sentinel |
| 2 | RANGE | Finite value outside configured plausibility bounds |
| 4 | COMMUNICATION | Sensor communication/acquisition failure; not MQTT connectivity |
| 8 | INVALID | Nonfinite numeric observation in the Python signal |
| 16 | ABRUPT | Causal step-change rule |
| 32 | STALE | Timestamp age rule when observation time is supplied |
| 64 | OUTLIER | Causal robust outlier rule |

Example: `{"quality_code":5,"quality_flags":"MISSING|COMMUNICATION"}`. Firmware implements bits 1/2/4 and shares names for the remaining reserved checks; it does not claim those checks run on ESP32. A failed DHT read is a missing-value sentinel, whereas Python's explicitly injected invalid reading is an invalid numeric observation. Neither becomes valid JSON NaN. Firmware JSON uses null; the optional ThingsBoard publisher omits unavailable scalar fields and preserves quality provenance.

## Sensor diagnostics

| Field | Python | Firmware |
| --- | --- | --- |
| environmental_sensor_status | OK (ambient channels remain available) | OK or ERROR from DHT finite-read outcome |
| gas_channel_status | OK / DISCONNECTED / TIMEOUT (controlled virtual diagnosis) | UNVERIFIED after ADC conversion, MISSING before acquisition |
| sensor_status | OK or DEGRADED for an acquisition fault | UNVERIFIED when acquisition completes, DEGRADED when a channel fails |

In Python, drift or invalid data can occur with completed acquisition; quality and injected `sensor_mode` carry that distinction. On ESP32, a zero, static or plausible ADC count cannot prove analog sensor health. There is no gas-presence or wiring diagnostic. The status LED means DHT acquisition and SD health, not verified gas-sensor health.

## Time

`timestamp` is ISO 8601 UTC when known, null in firmware JSON or blank in firmware CSV when unavailable. `timestamp_status` is SIMULATED_UTC (Python's deterministic clock), NTP_UTC (firmware epoch set through NTP), or UNSYNCHRONIZED. Firmware internal `epoch_s=0` is a sentinel and is never transmitted as a real 1970 timestamp. `uptime_ms` is a separate 64-bit monotonic duration since firmware boot, never UTC. Firmware event lines use explicitly labeled uptime milliseconds.

An NTP-derived clock is not a validated time reference; no clock uncertainty, holdover accuracy or continuous synchronization audit is implemented. Python's offline clock need not match today's date. The optional publisher rejects unavailable or timezone-naive timestamps rather than inventing the current time.

## Provenance, buffering and units

`node_id` and `sequence` identify attempts within one session; a future multi-session bridge needs a run identifier. `network_status`, `storage_status` and `buffered` describe acquisition-time provenance. A historical buffered flag remains true after synchronization. Current pending counts are separate. `scenario` describes Python's environment (NORMAL/HIGH_NH3) or WOKWI_SURROGATE; Python `sensor_mode` is independent. `simulated` is always true in this demonstrator.

Temperature is °C, RH is %, NH₃ and optional CO₂ are ppm. Firmware NH₃ fields are null/blank. Python `gas_raw` is an illustrative count-like signal without a 12-bit ADC limit; firmware `gas_raw` is 0–4095 ADC counts. Neither is a selective MQ2-to-NH₃ conversion. See the full [measurement model](measurement_model.md).

The revised firmware logs `/measurements-v2.csv` to avoid appending the new columns beneath an old header. Previous CSV consumers must migrate from singular `quality_flag` to `quality_code` and `quality_flags` and honor unavailable UTC.

# Synthetic measurement model and schema

All coefficients are illustrative engineering assumptions, not fitted farm observations. The default seed is 42; simulated UTC starts at 2026-01-01. Default sampling is 60 seconds. The dashboard advances one sample per wall-clock second when running; changing the interval affects simulated time, not UI refresh speed.

With elapsed days `d` and phase `p = 2πd`:

- Temperature = `22 + 4 sin(p) + N(0, 0.15)` °C.
- Relative humidity = `65 - 12 sin(p - 0.4) + N(0, 0.5)` %.
- Latent NH₃ = `9 + 3 sin(p - 0.8) + 0.12d + transient` ppm.
- Transients decay with a 900-second time constant. Each interval has event probability `1-exp(-interval/21600)` and an event adds 3–8 ppm.
- HIGH_NH3 adds 30 ppm while selected. It is a step increase, not a physiological model.
- CO₂ = `800 + 100 sin(p) + N(0, 8)` ppm; illustrative only.

The virtual low-cost NH₃ signal adds 2 ppm bias, 0.055 ppm per percentage-point humidity deviation from 65%, 0.09 ppm/°C deviation from 22 °C, 0.04 ppm/day drift and Gaussian noise with 0.65 ppm standard deviation. `Config` exposes these parameters. SENSOR_DRIFT adds a further 0.3 ppm per scenario sample; it is an accelerated commissioning fault.

The separate virtual reference adds 0.03 ppm bias, 0.002 ppm/day drift and 0.12 ppm standard-deviation noise. It shares the latent concentration but draws separate noise. It is not a real traceable reference. Python `gas_raw = 100 × raw NH₃` is a count-like illustrative signal, not MQ2 chemistry or a calibrated ADC equation. It is not restricted to a physical 12-bit range; no physical ADC response is inferred.

## Record schema

| Field | Type / units | Meaning |
| --- | --- | --- |
| timestamp | ISO 8601 UTC string | Simulated acquisition time |
| node_id | string | Measurement node |
| sequence | integer | Zero-based attempt identifier within the session |
| temperature_c | float, °C | Synthetic temperature |
| relative_humidity_pct | float, % | Synthetic relative humidity |
| gas_raw | float, illustrative counts | Analog-chain surrogate; firmware uses 12-bit ADC counts |
| nh3_raw_ppm | float/null/NaN, ppm | Synthetic low-cost NH₃ signal |
| nh3_calibrated_ppm | float/null, ppm | Fitted correction in exported validation dataset; unset in live acquisition |
| nh3_reference_ppm | float, ppm | Separate virtual reference |
| co2_ppm | float, ppm | Optional synthetic covariate |
| sensor_status | OK / DEGRADED | Aggregate virtual acquisition status |
| environmental_sensor_status | OK | Ambient acquisition status |
| gas_channel_status | OK / DISCONNECTED / TIMEOUT | Virtual gas-acquisition diagnosis |
| timestamp_status | SIMULATED_UTC | Synthetic clock provenance |
| quality_code | integer | Shared quality bitmask |
| sensor_mode | enum string | Independent gas fault selection |
| network_status | ONLINE / OFFLINE | Simulated acquisition-time transport state |
| storage_status | OK / FAILED | Acquisition-time local storage result |
| quality_flags | pipe-separated string | VALID or one or more quality flags |
| buffered | boolean | Acquired during network outage; not current synchronization state |
| scenario | NORMAL / HIGH_NH3 | Independent environmental condition |
| simulated | boolean | Always true |

CSV represents missing/nonfinite numbers with empty fields on pandas export; backend raw records preserve NaN. MQTT omits nonfinite fields and keeps the quality flags. The firmware exports null NH₃ fields and UTC or explicitly unsynchronized timestamps. Both producers expose quality_code and quality_flags. See the authoritative [schema contract](schema.md) for sensor diagnostics, quality bits, time and transport semantics. No live ingestion bridge is claimed.

## Quality decisions

Python checks temperature −20 to 60 °C, RH 0–100%, NH₃ 0–200 ppm (Python count-like values are not physical ADC counts). These are demonstration plausibility ranges. Missing, nonfinite and communication errors are flagged independently. Abrupt change defaults to 12 ppm between consecutive finite gas values. The causal outlier rule uses up to 30 preceding finite values, requires ten, and flags deviations beyond six robust standard deviations (`1.4826 × MAD`, floored at 0.25 ppm). An authentic concentration excursion may be flagged; flags require review, not deletion.

Freshness is evaluated when a caller supplies an observation time; a sample older than twice the interval is stale. Normal synthetic acquisition supplies current timestamps, so the dashboard will not invent stale data while paused. The freshness branch is tested independently. This demo does not detect a stuck sensor whose timestamps keep advancing.

Completeness is finite raw NH₃ values divided by all acquisition attempts, regardless of flags. Missing percentage includes null and nonfinite values. Valid count is a separate quantity. Independent ambient measurements remain visible during a gas sensor fault.

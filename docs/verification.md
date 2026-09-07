# Verification record — second engineering pass

## Verified locally

Observed on 2026-09-07 using Python 3.11 on Windows:

- `python -m pytest -q`: **17 passed**. Tests cover independent network/storage/sensor restoration in both orders, retained environment state, record accounting, repeated fault requests, quality encoding, strict telemetry JSON, missing timestamp rejection, known metrics and holdout leakage, plus all dashboard pages and fault controls.
- `python -m ruff check .`: passed.
- `python -m ruff format --check .`: passed.
- `python -m simulator`: generated 4,320 deterministic synthetic rows and calculated holdout metrics with the revised schema.
- `python -m platformio run -d firmware`: successful ESP32 compilation. This is not a hardware test.
- Streamlit started at localhost:8502. Headless Edge exercised eight pages and eight fault actions with no observed page errors or Streamlit exceptions. The updated Overview screenshot is an actual local render.
- The native C++ test command was attempted locally, but `g++` is not installed. No local native execution is claimed.

The default calibration remains an affine chronological holdout: 2,592 training rows and 1,728 validation rows. Calculated synthetic RMSE is 2.2183 ppm raw and 0.7102 ppm calibrated. These are virtual agreement metrics, not physical accuracy.

## Verified in CI

The workflow runs Python tests, lint, formatting, dataset generation, the native quality/serialization/queue test and ESP32 compilation. Execution status for this revision is pending publication and inspection; configuration alone is not a passing result.

## Verified in Wokwi

**Not verified.** The Community browser editor was opened and the diagram and compiled application upload were attempted. The simulation pane did not expose observable startup/serial output, and the browser reported a React error and an HTTP 401 resource response. No DHT, ADC, SD logging or WiFi runtime success is claimed. Exact modular source and custom-firmware browser steps remain in `wokwi/README.md`.

## Verified with external MQTT / ThingsBoard

**Not verified.** No external credentials were supplied and no live broker delivery was attempted. Local tests verify payload quality fields, strict JSON and rejection of unavailable timestamps only. ThingsBoard remains optional; the local dashboard is independent of it.

## Not yet physically validated

No ESP32 hardware, electrical interface, gas selectivity, calibration gases, reference traceability, farm campaign, response time, power-fail durability or laboratory accuracy was tested. Wokwi's direct AO connection is simulator-specific; a physical front end requires voltage-range, impedance, filtering, protection and calibration review.

Python pending queues are volatile and CSV is not automatically replayed after restart. Firmware rejects new telemetry when its 120-slot queue is full; an SD copy exists only if the local write succeeded. QoS 0 does not establish end-to-end acknowledgement. UTC availability, analog sensor health and data-quality status are explicitly separate.

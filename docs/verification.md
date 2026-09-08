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

GitHub Actions [run 34161935117](https://github.com/Rz-C137/agri-emissions-iot-digital-twin/actions/runs/34161935117) passed for implementation commit `1b61a3086e6c277654d9e82f3704418cddb4f90a`. Both jobs completed successfully:

- Python tests, lint, formatting and deterministic dataset generation.
- Native C++ compilation and execution of quality, serialization, timestamp and bounded-queue assertions on the Linux runner.
- ESP32 PlatformIO compilation.

These results were read from the actual job/step outcomes. This record identifies the tested implementation commit; a subsequent documentation-only commit records the evidence without claiming that it was the input to this run.

## Verified in Wokwi

**Not verified.** The Community browser editor was opened and the diagram and compiled application upload were attempted. The simulation pane did not expose observable startup/serial output, and the browser reported a React error and an HTTP 401 resource response. No DHT, ADC, SD logging or WiFi runtime success is claimed. Exact modular source and custom-firmware browser steps remain in `wokwi/README.md`.

## Verified with external MQTT / ThingsBoard

**Not verified.** No external credentials were supplied and no live broker delivery was attempted. Local tests verify payload quality fields, strict JSON and rejection of unavailable timestamps only. ThingsBoard remains optional; the local dashboard is independent of it.

## Not yet physically validated

No ESP32 hardware, electrical interface, gas selectivity, calibration gases, reference traceability, farm campaign, response time, power-fail durability or laboratory accuracy was tested. Wokwi's direct AO connection is simulator-specific; a physical front end requires voltage-range, impedance, filtering, protection and calibration review.

Python pending queues are volatile and CSV is not automatically replayed after restart. Firmware rejects new telemetry when its 120-slot queue is full; an SD copy exists only if the local write succeeded. QoS 0 does not establish end-to-end acknowledgement. UTC availability, analog sensor health and data-quality status are explicitly separate.


## Visual and hardware-presentation revision — 2026-09-08

- Four original SVGs were generated from checked wiring: hardware overview, exact pin connections, component reference and measurement chain. Browser rendering and text bounding-box collision checks passed for all four. These are configuration illustrations, not runtime or physical-validation images.
- The added Virtual Hardware page loads in Streamlit. The Python test suite remains **17 passed**, including navigation to all nine pages; Ruff lint and formatting passed.
- Headless Edge loaded the hardware assets and checked 1600, 1366, 760 and 390 pixel layouts with no page-level horizontal overflow or page errors. Fine pin labels should be opened/downloaded at full size on small screens. Overview cards were exercised with network and storage faults and showed OFFLINE, WRITE FAILURE and the actual queued counts.
- README and hardware-reference image paths were checked on disk. Updated Overview and Hardware-page screenshots are actual local dashboard captures in `docs/figures/`.
- A Wokwi browser upload was retried. The session again produced a React error and a 401 resource response without observable runtime/serial output. No `wokwi_runtime.png` is included or claimed.
- The firmware and scientific model were not modified by this visual revision. Earlier build and CI evidence above refers to the named tested implementation, not a new physical test.

- After publication, GitHub's rendered README loaded all three landing images, and the hardware-reference page rendered all four SVGs with nonzero natural dimensions. Images were inspected through the actual GitHub pages, not only local previews.
- GitHub Actions [run 34189586376](https://github.com/Rz-C137/agri-emissions-iot-digital-twin/actions/runs/34189586376) completed successfully for visual implementation commit `6ec4b96`: both Python and firmware jobs passed. A later evidence/screenshot-only commit records these observations.
# MARVELA-focused extension verification — 8 September 2026

- 22 Python tests passed, including all ten dashboard pages, a known Modbus CRC vector, register byte order, wrong-unit/CRC rejection, missing-reference preservation, committed-spool reopen, lost-ack deduplication, identity collisions and calibration artifact reload.
- Both 120-sample barn/manure CLI campaigns completed: 120 stored, 110 valid reference records, 10 reference fault records, zero pending after delivery recovery. Replaying the same campaign retained unique records.
- Ruff lint and format checks passed. The generated validation example reloads coefficients before holdout application; raw/calibrated RMSE is 2.2183/0.7102 ppm for synthetic NH3.
- Headless Edge rendered the commissioning campaign and both real component photos. Hardware page had no horizontal page overflow at widths 1366, 760 and 390 pixels; no browser page errors were observed. The new screenshot is an actual local dashboard capture.
- No new physical hardware, RS-485 electrical/timing test, MQTT broker test, flash power-loss test or farm campaign was performed. Existing firmware was not modified in this extension.
# Optional firmware Modbus bridge — local verification, 8 September 2026

Remote confirmation: [GitHub Actions run 34275815446](https://github.com/Rz-C137/agri-emissions-iot-digital-twin/actions/runs/34275815446) passed both jobs for implementation commit `81ff0f9`. Linux ran all 24 pytest cases, including compilation/execution of the native C++ Modbus runner; the existing native C++ quality test also passed. Both default and RS-485-enabled ESP32 builds passed in CI. The Windows-only native-test skip below does not represent a missing CI check.

- `python -m pytest -q`: 23 passed, 1 skipped locally. The skip is the native Modbus compile/run because this Windows environment has no host g++/clang++; Linux CI requires a compiler and executes it.
- `python -m ruff check .` and `python -m ruff format --check .`: passed.
- `python -m platformio run -d firmware -e esp32dev -e esp32dev_rs485`: both builds passed. Default RAM/flash: 51,564/829,641 bytes; optional RS-485: 51,580/831,213 bytes.
- `python -m simulator.campaign`: 120 stored, 110 valid references, 10 reference faults, zero pending after recovery.
- Dashboard AppTest exercised all ten pages; the running local Streamlit health endpoint returned `ok`.
- `python wokwi/export.py` refreshed browser sketch copies with the RS-485 path disabled by default. No Wokwi runtime or physical serial bus test was performed.
- Native cases and the cross-language wire contract are described in [Modbus firmware](modbus_firmware.md). UART electrical levels, direction timing, cable termination/bias and physical reference operation remain unmeasured. Reference output is a separate serial diagnostic, not part of the existing CSV/MQTT pipeline.

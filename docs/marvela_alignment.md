# From job requirements to an inspectable engineering demonstration

I designed this independent portfolio extension around public research needs, not an assumed MARVELA hardware bill of materials. No affiliation, consortium access or completed farm work is claimed.

## Evidence and scope

Checked on 8 September 2026: [CORDIS grant 101288134](https://cordis.europa.eu/project/id/101288134) identifies CH4, N2O and NH3, low-cost sensing and model-based tools, uncertainty reduction and agricultural validation. Its project period is September 2026–August 2030. These objectives motivate the three-gas interface fixture; they do not specify its concentrations or sensor technology.

The [official ATB job advertisement](https://www.leibniz-gemeinschaft.de/en/careers/jobs/detail/job/show/Job/scientist-postdoc-mfd-for-the-task-area-development-and-validation-of-iot-based-sensor-systems-for-environmental-monitoring), reference 2026-SM-3, emphasizes modular instrumentation, embedded integration, power, calibration, reference comparisons, campaigns and QA. It names I²C, SPI, UART, RS-485, Modbus, Ethernet and LoRaWAN as examples of interface knowledge. Neither source specifies an ESP32, MQ-2, DHT22, transceiver model or reference analyzer. All such selections here are my engineering choices. Related ATB projects are not evidence of MARVELA's hardware specification.

## Requirement-to-evidence matrix

| Need | Inspectable evidence | Boundary / next physical gate |
| --- | --- | --- |
| Modular electronics and acquisition | Existing C++ sensor, logger, quality and telemetry modules | Compiles; physical commissioning remains |
| Device interfaces | Host-tested Modbus RTU protocol logic in Python and ESP32 C++; optional UART2 transport | Physical RS-485 electrical commissioning remains future work; no I²C driver added |
| Continuous records and failures | Independent live-twin faults; new SQLite spool/reopen/idempotent receiver tests | SQLite is desktop disk, not ESP32 flash |
| Agricultural gases | New NH3, CH4, N2O register channels; barn/manure synthetic contexts | Fixtures, not mechanistic farm models or gas-selective hardware |
| Reference comparison | Chronological NH3 holdout, exported coefficients/hash, Bland–Altman view | Virtual reference is not a certified analyzer |
| QA and troubleshooting | Missing-reference/CRC/timeout flags; existing quality bitmask | Bench electrical noise, drift and traceability remain |
| Campaigns and coordination | Staged protocol below with explicit handover artifacts | Proposed workflow, no claimed partner coordination |
| Power supply integration | Power and wiring review below | No measured load budget or brownout validation |
| Ethernet / LoRaWAN | Design choice discussion | Future integration; no stack claimed |

## Run the new experiment

```bash
python -m simulator.campaign
python -m simulator.campaign --site manure --output data/runs/manure
python -m validation.report
python -m pytest -q
```

The dashboard's **Commissioning Bench** exposes request/response bytes and fault selection. The CLI writes `node.sqlite`, `receiver.sqlite`, `campaign.json` and `summary.json` to its output directory. The default campaign has 120 attempts, 110 valid reference records and 10 flagged records. Network delivery is withheld for indices 20–79 and then recovered. Timeout indices are 30–34; CRC corruption 60–64. These are scripted sample windows, not wall-clock serial timeouts. Retransmission after receiver commit and before local acknowledgement is tested separately. Reopening tests recovery of committed records, not arbitrary power failure during filesystem writes.

![Actual local commissioning dashboard with synthetic records](figures/commissioning_dashboard.png)

See the generated [example validation report](validation_example/report.md), [coefficient artifact](validation_example/calibration.json) and [full metrics](validation_example/metrics.json). Regenerate with `python -m validation.report --output docs/validation_example`.

The original Twin queues and ESP32 queues remain volatile. The new local receiver is an in-process SQLite mock transport, not an MQTT broker or a Streamlit-to-ESP32 bridge. It has no capacity management: disk-full failures propagate. It is not a tested internal-flash fallback. Repeated runs replay the same identities idempotently; use a new directory for independent experiments. A different payload under an existing identity is rejected.

### Modbus contract selected for the virtual reference

Unit 1, function 03, start offset 0, quantity 3. This is an invented demonstrator map, never a manufacturer's register map. Payload words are unsigned big-endian; the CRC is appended low byte first. Empty responses raise timeout; malformed, wrong-unit, wrong-function or wrong-size responses are rejected. The emulator intentionally supports only this request, not the complete protocol or serial timing.

| Zero-based register offset | Quantity | Encoding | Range |
| --- | --- | --- | --- |
| 0 | NH3 | uint16 / 100 ppm | 0–655.35 ppm |
| 1 | CH4 | uint16 / 100 ppm | 0–655.35 ppm |
| 2 | N2O | uint16 / 1000 ppm | 0–65.535 ppm |

These ranges describe encoding capacity, not instrument performance. Values are minute-index sinusoids: NH3 = 12 + 4 sin(p), CH4 = 8 + 3 sin(p + 0.5), N2O = 0.6 + 0.2 sin(p + 1), p = 2πi/60. The manure fixture multiplies them by 1.5. Raw channels add selected biases of 2, 0.8 and 0.08 ppm plus deterministic small perturbations. The reference rounds the fixture into registers. This simplified protocol fixture is separate from the existing richer noisy NH3 validation model; neither is measured farm evidence.

Protocol sources: [Modbus specifications](https://www.modbus.org/modbus-specifications) and [serial-line guide V1.02](https://modbus.org/docs/Modbus_over_serial_line_V1_02.pdf).

## Pin plan: implemented node and proposed industrial extension

Use GPIO labels, not the physical row positions of a board photograph. See [real component photographs and current diagram](hardware.md). Verify the exact board revision before assembly; ESP32 variants with PSRAM may reserve GPIO16/17.

| Connection | ESP32 GPIO | Status and electrical meaning |
| --- | --- | --- |
| DHT22 DATA | 4 | Implemented; 10 kΩ pull-up to 3.3 V; VCC 3.3 V, common GND; bare sensor NC unused |
| MQ-2 AO | 34 / ADC1 | Implemented only as simulator analog surrogate; direct 5 V-module AO is not approved physical wiring |
| microSD SCK / MISO / MOSI / CS | 18 / 19 / 23 / 5 | Implemented SPI, compatible 3.3 V module; check GPIO5 strapping at startup |
| I²C SDA / SCL | 21 / 22 | Reserved proposal; pull-ups to 3.3 V sized for actual bus capacitance; no I²C instrument simulated |
| UART2 TX / RX | 17 / 16 | Optional firmware UART2 transport; disabled by default |
| RS-485 driver direction | 27 | Optional firmware combined DE and active-low RE control |

For a **proposed MAX3485** 3.3 V transceiver, TX17 goes to DI (package pin 4), RO (pin 1) to RX16, GPIO27 to DE (pin 3) and active-low RE (pin 2). LOW receives, HIGH transmits. VCC pin 8 goes to 3.3 V, GND pin 5 to logic return, with local decoupling. A pin 6 and B pin 7 form the differential pair. This plan comes from the [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX3483-MAX3491.pdf), not MARVELA. It requires a physical bench check; do not substitute a 5 V transceiver breakout without verifying logic levels.

Use twisted pair and terminate only at the two physical bus ends with resistance matched to cable impedance (often 120 Ω). Establish idle bias at one designed location; check transceiver common-mode limits, surge protection, grounding and isolation for farm cabling. A/B vendor naming can differ: verify signal polarity from both datasheets. In a real UART implementation, release DE only after the last stop bit, enforce RTU frame spacing and configure matching baud/parity; the optional firmware handles TX completion and frame gaps, but physical timing is unmeasured. Proposed starting configuration: 9600 baud, 8E1, unit 1, confirmed against the actual instrument manual.

RS-485 is the electrical link; Modbus defines messages and register meaning. The ESP32 UART needs the external transceiver. I²C is intended for short local sensor connections; SPI serves the local SD; neither replaces the farm cable interface.

### Power and environmental integration

Before a physical build, make a measured current budget for MCU/WiFi peaks, SD write peaks, gas-sensor heaters, reference interfaces and conversion losses. Choose a regulated supply with verified transient margin, protected input and appropriate fusing. Follow the [Espressif board power instructions](https://docs.espressif.com/projects/esp-idf/en/v4.2/esp32/hw-reference/esp32/get-started-devkitc.html): do not simultaneously feed alternative power inputs. Separate noisy heater/motor power paths from analog returns, provide local decoupling and verify ADC conditioning with a meter/oscilloscope. Select enclosure, cable glands, condensation control and maintainable connectors for the actual installation.

Bench tests should step load, interrupt supply, remove SD and inject communication faults while checking reset cause, timestamp validity and record loss. An internal-flash fallback would need bounded capacity, wear accounting and atomic recovery; the desktop SQLite spool cannot establish those properties.

## Step-by-step laboratory-to-farm workflow

These are proposed engineering stages, not completed experiments or an official MARVELA protocol.

1. **Agree measurement questions.** Record gas species, concentration ranges, livestock/manure context, response time, uncertainty target and decision use with the scientific lead. Separate concentration monitoring from emission estimation; the latter additionally needs a justified ventilation/flux method and uncertainty propagation. Gate: signed requirements, not arbitrary accuracy promises.
2. **Freeze the interface contract.** Obtain actual sensor/reference datasheets, serial numbers, calibration certificates, units, wet/dry basis, register maps, baud/parity, warm-up times and status codes. Gate: reviewed wiring and power budget, electrical limits and instrument-specific drivers.
3. **Commission the electronics.** Check continuity unpowered, then rails and current limits, GPIO levels, ADC protection, SD integrity and serial waveforms. Record firmware revision, configuration, node ID, reset reason and clock synchronization. Gate: repeatable power-up and diagnosed disconnects with no invented valid readings.
4. **Plan calibration.** With the responsible laboratory team, choose approved reference methods and standards, zero/span sequence, randomized levels, repeated runs and temperature/RH blocks. Follow laboratory gas-handling procedures. Log uncertainty/certificates, stabilization criteria and sample-line effects; NH3 adsorption and humidity sensitivity need explicit evaluation. Gate: traceable raw records and an agreed uncertainty budget.
5. **Fit only the calibration block.** Preserve immutable raw data and flags; align instrument clocks and account for response lag using the training data. Export versioned coefficients, units, range, source hash and training period. Do not optimize delay or coefficients using the holdout. Gate: reproducible calibration artifact.
6. **Validate independently.** Use later days and preferably held-out devices/sites, retain missing rows in completeness, compare bias/RMSE and concentration-dependent residuals, agreement limits, repeatability and drift. Include reference, sampling, calibration and temporal uncertainties. Gate: predefined scientific acceptance criteria; virtual RMSE is not a physical pass mark.
7. **Challenge reliability.** Disconnect reference/network/storage, corrupt frames, restart after commit, remove power under controlled conditions and document lost IDs. Measure outage and post-restoration backlog time separately. Gate: loss/recovery accounting and explicit limits, not a blanket zero-loss claim.
8. **Pilot in livestock and manure settings.** Agree placement, sampling lines, co-location, maintenance, clock checks, metadata and pre/post checks with farm partners. Record operational events and environmental context. Gate: pilot review before wider deployment; real campaign datasets stay distinct from this synthetic repository.
9. **Handover and report.** Deliver versioned schemas, wiring, firmware, calibration artifacts, QA decisions, deviations and analysis scripts with an owner/date/action issue log. Review interpretation jointly and draft methods/results from actual evidence. Publications and partner coordination remain future work, not portfolio experience claims.

## Firmware protocol bridge

The same narrow FC03 contract now has a host-testable C++ parser/client and an optional UART2 adapter. See [the shared protocol contract and enablement instructions](modbus_firmware.md). Protocol tests do not validate the RS-485 electrical bus.

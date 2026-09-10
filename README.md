# Digital Twin and Virtual Commissioning of an IoT-Based Agricultural Emission Monitoring System

**A virtual prototype for continuous environmental and gaseous-emission monitoring in livestock facilities**

I built this repository to show the full measurement chain I inspected: livestock monitoring context → sensors → ESP32 wiring → firmware → compilation → virtual hardware → local logging → telemetry → dashboard → fault injection → calibration and validation — plus a separate Modbus RTU commissioning bench for industrial-style reference acquisition.

![Streamlit overview — synthetic measurements and system state](docs/figures/dashboard_overview.png)

*Authentic local dashboard capture. All measurements are synthetic; no physical farm data.*

![Measurement chain — acquire, retain, communicate](docs/figures/measurement_chain.svg)

*Conceptual end-to-end path. Python runs the offline twin; ESP32/Wokwi demonstrates embedded acquisition. Streamlit does not ingest live ESP32 telemetry.*

![Virtual hardware layout](docs/figures/virtual_hardware_overview.svg)

*Virtual wiring derived from `wokwi/diagram.json` and `firmware/include/Config.h`. MQ-2 is used only as an analog gas-acquisition surrogate. It is not treated as a selective NH₃ sensor.*

![Exact ESP32 pin connections](docs/figures/esp32_pin_connections.svg)

*Signal names and power nets checked against firmware configuration.*

**Research-focused extension:** [MARVELA / ATB requirement mapping and laboratory-to-farm workflow](docs/marvela_alignment.md), a three-gas **Modbus RTU commissioning bench**, durable local recovery tests, and [an eight-minute interview route](docs/interview_walkthrough.md). This is an independent portfolio response to public needs, not a MARVELA deliverable.

## Hands-on implementation

| Stage | Where to look |
| --- | --- |
| Monitoring context | [Measurement model](docs/measurement_model.md) · barn/manure synthetic fixtures |
| Real components | [Hardware reference](docs/hardware.md) · [attributed photos](docs/figures/photos/ATTRIBUTION.md) |
| Wiring + pins | [Pin diagram](docs/figures/esp32_pin_connections.svg) · [Wokwi `diagram.json`](wokwi/diagram.json) |
| Firmware | [`firmware/`](firmware/) · [Modbus contract](docs/modbus_firmware.md) |
| Virtual circuit | [Wokwi setup](wokwi/README.md) |
| Live twin | [Overview](docs/figures/dashboard_overview.png) · [Virtual Hardware](docs/figures/hardware_dashboard.png) |
| Fault handling | Dashboard **Fault Injection** page |
| Modbus bench | [Commissioning dashboard](docs/figures/commissioning_dashboard.png) · `python -m simulator.campaign` |
| Calibration | Dashboard **Calibration & Validation** · [example report](docs/validation_example/report.md) |
| Job alignment | [MARVELA / ATB matrix](docs/marvela_alignment.md) |

## End-to-end implementation path

### 1. Monitoring objective

I framed the prototype around livestock-building air monitoring: temperature, humidity and cross-sensitive gas indicators for commissioning workflows before any physical deployment.

### 2. Sensors and acquisition hardware

DHT22 provides digital environmental readings. MQ-2 stands in for an analog gas channel only. ESP32 aggregates signals; microSD provides local CSV logging over SPI. Real component photographs (ESP32, DHT22) are attributed separately from the virtual wiring diagrams — see [hardware reference](docs/hardware.md).

![Component roles](docs/figures/prototype_components.svg)

### 3. Wiring and interfaces

I implemented and checked: DHT22 DATA → GPIO4 (10 kΩ pull-up), gas AO → GPIO34, microSD CS/SCK/MISO/MOSI → GPIO5/18/19/23, 3.3 V and GND for DHT22/SD, and a simulator-only MQ-2 supply on VIN. An optional UART2 RS-485 path (GPIO16/17/27) is documented for the industrial extension but disabled by default.

### 4. Firmware implementation

`firmware/` contains PlatformIO modules for configuration, acquisition, QA/QC, SD logging, telemetry, faults and system state. Host-tested Modbus RTU logic is shared between Python and C++; physical RS-485 commissioning remains future work.

### 5. Virtual hardware and browser simulation

The Wokwi `diagram.json` reproduces the same pin contract. I export browser files with `python wokwi/export.py` after firmware edits.

### 6. Local monitoring and fault handling

The Streamlit dashboard exposes sensor, network, storage and quality state. **Fault Injection** changes each subsystem independently; I verified pending telemetry during simulated outages.

### 7. Calibration and validation

A fixed dataset supports affine correction with chronological holdout, bias/MAE/RMSE/R² and residual plots against a virtual reference — not ground truth. Regenerate artifacts with `python -m validation.report`.

### 8. Industrial commissioning bench

The **Commissioning Bench** page exercises Modbus RTU request/response bytes, CRC faults and timeouts against a three-gas virtual reference (NH₃, CH₄, N₂O). The CLI campaign writes SQLite spool/receiver databases with scripted outage and recovery windows — desktop persistence, not proven ESP32 flash durability.

![Commissioning bench](docs/figures/commissioning_dashboard.png)

### 9. Why this matters for the target role

| Capability | How this repository shows it |
| --- | --- |
| Modular IoT sensor systems | Firmware modules + offline twin + commissioning bench |
| Sensor integration | DHT22 + analog surrogate + QA/QC flags |
| Microcontroller programming | ESP32 scheduler, ADC, SPI, optional UART2 |
| Communication interfaces | SPI SD, UART/Modbus RTU, optional MQTT |
| Data loggers | microSD + session CSV + SQLite campaign spool |
| Automated acquisition | Timed sampling loops + campaign CLI |
| Calibration / validation | Holdout workflow, exported coefficients, Bland–Altman view |
| Troubleshooting / robustness | Fault injection + Modbus fault modes + queue retention |

Full requirement-to-evidence mapping: [MARVELA / ATB alignment](docs/marvela_alignment.md).

## What this prototype demonstrates

- Embedded data acquisition: DHT22 digital readings, analog gas-surrogate ADC and SPI microSD logging.
- Shared Python/C++ Modbus RTU client contract: host-tested protocol logic and optional ESP32 UART2 transport, disabled by default.
- IoT communication: offline queue simulation, optional TLS MQTT and separate ESP32 MQTT firmware.
- Resilient logging and fault handling: acquisition during simulated network failure, visible pending records and synchronization events.
- Digital-twin monitoring: sensor, network, storage and data-quality states, including concurrent faults.
- Measurement QA/QC: ranges, missing values, abrupt changes, freshness and causal outlier flags without deleting raw data.
- Calibration workflow: affine correction, chronological holdout, bias, MAE, RMSE, R² and residual analysis.
- Commissioning campaign: SQLite local spool, idempotent receiver, reopen/recovery tests and three-gas reference fixture.

## Quick start

Use Python 3.10+. From this repository:

```bash
python -m venv .venv
```

Activate on Windows PowerShell: `.venv\Scripts\Activate.ps1`. On macOS/Linux: `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python -m streamlit run dashboard/app.py
```

Open the local URL printed by Streamlit. The initial session contains two hours of deterministic synthetic measurements. No `.env`, broker, ThingsBoard account or Wokwi session is needed.

Regenerate figures, datasets and checks:

```bash
python tools/generate_figures.py
python -m simulator
python -m simulator.campaign
python -m validation.report
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

`data/demo.csv` and `data/demo.metrics.json` contain calculated virtual results. Campaign output goes under `data/runs/`. Stop the server with Ctrl+C.

## Motivation and measurement scope

I use virtual commissioning to make acquisition and fault-handling decisions inspectable before physical deployment. Livestock monitoring combines variable environmental conditions, cross-sensitive instruments, unreliable communications and difficult maintenance. A plausible-looking chart alone cannot establish a valid measurement system.

I therefore expose raw observations, quality flags and transport states separately. A finite but flagged value counts toward availability, not toward validity.

## Embedded implementation and browser simulation

`firmware/` hardware-dependent acquisition is isolated from the plain C++ quality function. See [firmware instructions](firmware/README.md) and [Wokwi browser setup](wokwi/README.md).

The firmware does not calculate NH₃ from MQ2 voltage. DHT diagnostics and analog gas-channel status are separate; plausible ADC counts leave analog sensor health UNVERIFIED. MQTT is unconfigured by default. The firmware RAM queue holds 120 records; QoS 0 publishing does not prove delivery. See [implementation limits](docs/limitations.md).

## Digital twin and fault injection

The twin represents measurement-system operational state, not a complete livestock building. Use **Fault Injection** to change the synthetic environment, gas-acquisition mode, network and storage independently. Restore sensor, network or storage separately; **Restore all faults** restores all three infrastructure faults and leaves the environment unchanged.

During network failure, local acquisition continues and pending telemetry grows. **Restore network only** services pending telemetry on the next sample without clearing sensor or storage faults. Queues are volatile and do not survive process termination.

## QA/QC, calibration and validation

I preserve raw data and attach quality information. The calibration page uses a separate fixed dataset so injected faults cannot silently change the benchmark. A linear model is fitted on valid pairs in the first 60% of the time series; all finite pairs in the final 40% are evaluated.

The simulated reference has its own uncertainty and is not ground truth. Example artifacts: [validation report](docs/validation_example/report.md), [coefficients](docs/validation_example/calibration.json).

## What this prototype does not claim

- Measurements are simulated; no physical farm measurement campaign is claimed.
- MQ-2 is not a selective NH₃ sensor or reference instrument.
- Wokwi and compilation are not physical validation.
- SQLite campaign persistence is not proven embedded flash durability.
- Virtual validation is not laboratory or field validation.
- No MARVELA affiliation, regulatory compliance or laboratory traceability is established.

## Documentation

Start with [job alignment and staged experiments](docs/marvela_alignment.md), then [design decisions](docs/design_decisions.md) and [technical questions](docs/technical_questions.md).

| Document | Purpose |
| --- | --- |
| [MARVELA / ATB alignment](docs/marvela_alignment.md) | Requirement matrix, pin plan and laboratory-to-farm gates |
| [Interview walkthrough](docs/interview_walkthrough.md) | Eight-minute demonstration route |
| [Hardware](docs/hardware.md) | Wiring figures, photos and front-end limits |
| [Modbus firmware](docs/modbus_firmware.md) | Shared RTU contract and UART2 transport |
| [Architecture](docs/architecture.md) | Modules, data flow and state machine |
| [Measurement model](docs/measurement_model.md) | Synthetic equations, units and QA/QC |
| [Validation protocol](docs/validation_protocol.md) | Holdout method and lab extension |
| [Limitations](docs/limitations.md) | Scientific and implementation boundaries |
| [Verification](docs/verification.md) | Checks run and evidence limits |
| [Interview demo](docs/interview_demo.md) | Short scripts |
| [ThingsBoard](thingsboard/README.md) | Optional TLS MQTT setup |

## Future physical implementation

I would select an NH₃-appropriate instrument and reference method, characterize cross-sensitivity and drift in controlled conditions, validate signal conditioning and power protection, and evaluate ingress protection, contamination, condensation, cleaning, maintainability and placement. A durable acknowledged outbox, clock synchronization audits, independent validation and ventilation measurements would precede any emission-rate interpretation.

## License

MIT — see [LICENSE](LICENSE). Component photographs retain their own CC BY-SA 4.0 licenses; see [attribution](docs/figures/photos/ATTRIBUTION.md).

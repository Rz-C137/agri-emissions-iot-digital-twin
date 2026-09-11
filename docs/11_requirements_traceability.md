# Requirements Traceability and Evidence Status

This is the authoritative source for implementation and evidence status. Other documents, README text, dashboard labels, and figure captions must not claim a higher level than this table.

| Requirement | Artifact | Evidence level | Current status |
|---|---|---|---|
| Measurement problem and farm context | `01_project_scope.md`, `02_farm_context.md` | Design context | LVAT-like representative scenario |
| Sensor selection and procurement | `03_sensor_selection.md` | Engineering design | Selection documented; procurement pending |
| Microcontroller programming | `firmware/` | Implemented / build-tested | ESP32 firmware compiles |
| Virtual sensor integration | `wokwi/diagram.json`, `firmware/` | Virtual / implemented | Pin-exact source and firmware paths |
| Firmware pin contract | `firmware/include/Config.h` | Implemented source contract | Automated consistency check required |
| Wiring | `05_wiring_and_interfaces.md` | Virtual/design-stage | Physical wiring pending |
| Digital, 1-Wire, I2C, SPI and ADC interfaces | `firmware/`, `wokwi/` | Implemented in software/virtual | No physical electrical evidence |
| UART/RS-485/Modbus | `firmware/`, `simulator/`, tests | Software implemented and host-tested | Physical transceiver/bus pending |
| Data logging | `Logger.cpp`, Python run logs | Implemented in software/virtual | Physical SD test pending |
| WiFi/MQTT | `Telemetry.cpp`, `thingsboard/` | Implemented/documented | No live external broker validation |
| QA/QC and fault handling | `QualityControl.cpp`, `simulator/`, dashboard | Implemented in software/virtual | No physical fault campaign |
| Temperature disagreement | firmware QA/QC and Sensor Commissioning page | Virtual / test-covered | DHT22/DS18B20/BMP180 comparison |
| Calibration and validation | `validation/`, `08_validation.md` | Synthetic workflow | No physical accuracy claim |
| Driver installation/configuration | `06_driver_configuration.md` | Documented | Host installation evidence pending |
| Commissioning | `07_commissioning.md`, `physical_prototype/` | Virtual workflow/design-stage | Bench record pending |
| Soldering and physical assembly | `physical_prototype/` | Future physical implementation | No assembly evidence yet |
| Prototype carrier PCB | `hardware/kicad/`, `09_physical_bench_plan.md` | Design-stage | No fabricated/tested PCB |
| Field deployment | `10_deployment_concept.md` | Design-stage | No farm installation or campaign |

## Verified software checks

These commands are the current verification baseline:

```powershell
python -m pytest -q
ruff check .
python -m compileall -q dashboard simulator validation
python -m platformio run -d firmware
python tools/prepare_wokwi_firmware.py
```

A successful firmware build is not a hardware test. Wokwi runtime evidence is reported only when an actual successful runtime session and serial output are captured.

# Bench-to-Barn Demonstrator

A modular IoT livestock-monitoring node for a representative, LVAT-like livestock research environment. The repository follows one engineering workflow:

```text
measurement problem -> sensor requirements -> selection/procurement
-> interfaces/wiring -> ESP32 firmware -> acquisition -> QA/QC
-> local storage/communication -> fault handling -> commissioning
-> synthetic validation -> physical bench plan -> future deployment
```

## Evidence boundary

- **Implemented / verified:** modular firmware builds, Python tests, deterministic virtual twin, dashboard QA/QC, and host-tested Modbus protocol logic.
- **Virtual / simulated:** Python measurements, fault injection, calibration data, and Wokwi circuit integration.
- **Design-stage / future physical implementation:** procurement, breadboard assembly, soldering, measured voltages, physical RS-485, reference validation, PCB fabrication, and farm deployment.

The authoritative status is [docs/11_requirements_traceability.md](docs/11_requirements_traceability.md).

## System

Phase 1 virtual embedded node:

- DHT22: temperature/RH, digital GPIO4
- DS18B20: redundant temperature, 1-Wire GPIO15
- BMP180: temperature/pressure, I2C GPIO21/22
- MQ-2: analog acquisition surrogate only, ADC GPIO34
- microSD: SPI logging, CS GPIO5 and SCK/MISO/MOSI GPIO18/19/23
- optional RS-485/Modbus firmware path: UART2 GPIO16/17, direction GPIO27

The single wiring contract is `firmware/include/Config.h` plus `wokwi/diagram.json`; the physical wiring interpretation is [docs/05_wiring_and_interfaces.md](docs/05_wiring_and_interfaces.md).

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
streamlit run dashboard/app.py --server.port 8502
```

Open `http://localhost:8502`. The dashboard has four pages:

1. Overview
2. Sensor Commissioning
3. Hardware & Architecture
4. Validation / QA/QC

The dashboard is a local commissioning interface for the Python twin. It is not a live ESP32-to-Streamlit bridge.

## Wokwi workflow

Wokwi remains the embedded-simulation layer for pin-exact wiring and firmware execution.

1. Build the firmware:

   ```powershell
   python -m platformio run -d firmware -e esp32dev
   ```

2. Prepare browser/Wokwi artifacts:

   ```powershell
   python tools/prepare_wokwi_firmware.py
   ```

3. Open `wokwi/diagram.json` with Wokwi for VS Code, or open a new ESP32 project in the Wokwi editor.
4. For the browser editor, use its **Upload Firmware and Start Simulation** action with the prepared firmware binary. Wokwi runtime and serial output are only claimed when actually observed.
5. After firmware changes, refresh the browser-compatible files with `python wokwi/export.py` where applicable.

The repository does not use an experimental Streamlit Wokwi iframe as a runtime dependency.

## Documentation

- [Project scope](docs/01_project_scope.md)
- [Farm context](docs/02_farm_context.md)
- [Sensor selection and procurement](docs/03_sensor_selection.md)
- [System architecture](docs/04_system_architecture.md)
- [Wiring and interfaces](docs/05_wiring_and_interfaces.md)
- [Driver configuration](docs/06_driver_configuration.md)
- [Commissioning](docs/07_commissioning.md)
- [Validation and QA/QC](docs/08_validation.md)
- [Physical bench plan](docs/09_physical_bench_plan.md)
- [Deployment concept](docs/10_deployment_concept.md)
- [Requirements traceability](docs/11_requirements_traceability.md)
- [Limitations](docs/12_limitations.md)

## Interview demonstration

Show the dashboard Overview and Sensor Commissioning pages, then Hardware & Architecture for the pin map, Wokwi source, firmware build and system flow. State clearly which evidence is virtual and which physical bench work remains.

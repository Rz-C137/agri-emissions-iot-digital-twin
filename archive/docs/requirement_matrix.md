# Job Requirement → Demonstrator Matrix

Maps the [ATB/MARVELA microcontroller vacancy](https://loai-comramo.pi-asp.de/bewerber-web/?company=*-FIRMA-ID&tenant=1022_LOAI&lang=D#position,id=2f2c1071-b1e0-42c9-9a00-b705abf697c4,popup=y) and David Janke’s hands-on criteria to **concrete repository artifacts**.

| Requirement / keyword | How we demonstrate | Artifact | Status |
|---------------------|-------------------|----------|--------|
| Modular IoT sensor systems | Layered firmware + twin | `firmware/`, `src/agri_twin/` | ✅ |
| Selecting sensors from scratch | Criteria tables, rejections | [sensor_procurement.md](sensor_procurement.md) | 📋 |
| Procuring sensors | BOM, vendor log | [hardware_selection.md](hardware_selection.md), procurement log | 📋 |
| Integrating sensors | Multi-bus firmware + Wokwi | `wokwi/diagram.json`, `Sensors.cpp` | 🔄 expand DS18B20/BMP180 |
| Wiring | Pin map, diagram | [hardware.md](hardware.md), `diagram.json` | ✅ / 🔄 |
| Soldering | Assembly photos, joint notes | `physical_prototype/photos/` | ⏳ real photos TBD |
| Installing drivers (firmware) | Library init docs | [driver_configuration.md](driver_configuration.md) | 📋 |
| Configuring drivers (host) | USB-UART, PlatformIO | [hardware_commissioning.md](hardware_commissioning.md) | 📋 |
| Microcontroller programming | ESP32 C++ | `firmware/src/` | ✅ |
| Data loggers | microSD CSV | `Logger.cpp` | ✅ |
| Power supplies | Schematic section | [circuit_design.md](circuit_design.md) | 📋 design |
| I²C | BMP180 / SCD41 | `Scd41.cpp`, planned BMP180 | 🔄 |
| SPI | microSD | `Logger.cpp` | ✅ |
| UART / RS-485 | Modbus transport | `Rs485Transport.cpp` | ✅ software |
| Modbus | Shared Python/C++ tests | `ModbusRtu.*`, pytest | ✅ |
| WiFi / MQTT | Telemetry | `Telemetry.cpp` | ✅ |
| Laboratory tests | Bench protocol | [bench_commissioning_report.md](bench_commissioning_report.md) | ⏳ |
| Calibration | Methodology + twin | [validation_protocol.md](validation_protocol.md) | 📋 |
| Farm / manure context | LVAT-like scenario | [farm_context.md](farm_context.md) | 📋 |
| Validation vs reference | Modbus reference path | RS-485 bench + twin | 🔄 |
| QA/QC procedures | Quality flags | `Quality.h`, dashboard | ✅ |
| Measurement protocols | CSV schema, commissioning | [schema.md](schema.md) | ✅ |
| Technical documentation | `docs/` tree | This repo | ✅ |
| Data analysis (Python) | Dashboard, validation | `dashboard/`, pytest | ✅ |
| Troubleshooting | Log template | `physical_prototype/troubleshooting/` | ⏳ |
| PCB / robust system | KiCad proposal | `hardware/kicad/` (planned) | ⏳ |
| Scientific reporting | MARVELA alignment | [marvela_alignment.md](marvela_alignment.md) | ✅ |

**Legend:** ✅ done · 📋 documented · 🔄 in progress · ⏳ needs real hardware/evidence

## David Janke email — explicit mapping

| Phrase in email | Demonstrator response |
|-----------------|----------------------|
| Selecting and procuring sensors | [sensor_procurement.md](sensor_procurement.md) |
| Integrating into measurement system | Wokwi + firmware + pin map |
| Wiring or soldering at interfaces | `physical_prototype/` + future KiCad |
| Installing and configuring drivers | [driver_configuration.md](driver_configuration.md) + [hardware_commissioning.md](hardware_commissioning.md) |
| Installing and commissioning on site | [farm_context.md](farm_context.md) + commissioning report |
| Substantial on-site / lab presence | Bench + LVAT-like field narrative (honest stage) |

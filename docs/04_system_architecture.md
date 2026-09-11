# System Architecture

## Authoritative layers

| Layer | Authoritative implementation | Evidence level |
|---|---|---|
| Embedded acquisition | `firmware/src/`, `firmware/include/` | Implemented / build-tested |
| Virtual wiring | `wokwi/diagram.json` | Virtual / source configuration |
| Python twin | `simulator/` | Virtual / test-covered |
| Dashboard | `dashboard/` | Implemented as local commissioning UI |
| Validation workflow | `validation/` | Virtual / synthetic data |
| External publishing | `thingsboard/` | Optional, not live-validated |

## Data path

```text
livestock environment
 -> DHT22 / DS18B20 / BMP180 / analog surrogate
 -> ESP32 acquisition and timestamps
 -> quality flags and fault state
 -> microSD local logging
 -> RS-485/Modbus reference path
 -> WiFi/MQTT optional transport
 -> local storage and Streamlit QA/QC
 -> calibration and validation workflow
```

The Python twin and ESP32 firmware are separate producers. Streamlit does not ingest live ESP32 telemetry.

## Firmware modules

- Sensor drivers: DHT22, DS18B20, BMP180 and analog acquisition.
- `SensorManager`: acquisition coordination.
- `QualityControl`: temperature disagreement and measurement flags.
- `Logger`: SD/CSV role.
- `Telemetry`: WiFi/MQTT queue and retry role.
- `ModbusRtu` and `Rs485Transport`: protocol and optional UART path.
- `FaultManager` and `SystemState`: operational state and counters.

## Delivery boundaries

Firmware and Python queues are bounded or session-scoped according to their implementation. MQTT QoS and local queue acceptance do not establish durable end-to-end delivery. These are software behaviours, not physical reliability or farm validation claims.

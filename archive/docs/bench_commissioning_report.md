# Bench Commissioning Report

**Status:** Template — replace `TBD` with **measured** values only after real tests.

**Node:** _______________  
**Firmware environment:** `esp32dev` / `esp32dev_scd41` / `esp32dev_rs485`  
**Date:** _______________

## Summary

| Area | Result | Evidence |
|------|--------|----------|
| Power rails | TBD | `physical_prototype/commissioning/voltage_measurements.csv` |
| Environmental sensor | TBD | `sensor_test_results.csv` |
| microSD logging | TBD | Serial + file on card |
| RS-485 Modbus | TBD | `rs485_test_results.csv` |
| MQTT / WiFi | TBD | Optional; not required for bench sign-off |

## Electrical measurements

| Test | Expected | Measured | Pass/Fail |
|------|----------|----------|-----------|
| 3.3 V rail (ESP32) | 3.2–3.4 V | TBD | |
| Analog input idle (GPIO34) | Stable baseline | TBD | |
| I²C bus (SCD41 present) | Device 0x62 ACK | TBD | |

## Functional tests

| Test | Method | Expected | Observed | Result |
|------|--------|----------|----------|--------|
| Boot / serial | 115200 baud | CSV every 5 s | TBD | |
| DHT22 or SCD41 | Compare to reference hygrometer / known CO₂ | Within stated sensor spec | TBD | |
| SD write | Power cycle, re-read file | Row count increases | TBD | |
| Sensor disconnect | Unplug DHT or SCD41 | `environmental_sensor_status=ERROR` | TBD | |
| RS-485 CRC | Host injects bad frame | `CRC_ERROR` status | TBD | |
| RS-485 timeout | No slave response | `TIMEOUT` status | TBD | |

## Physical assembly notes

_Describe soldering, wire gauge, enclosure, and any rework. Link photos in `physical_prototype/photos/`._

TBD

## Open issues

| ID | Issue | Impact | Next step |
|----|-------|--------|-----------|
| | | | |

## Sign-off

This report is valid only when populated with real measurements and photos from the bench.

| Role | Name | Date |
|------|------|------|
| Commissioning engineer | | |

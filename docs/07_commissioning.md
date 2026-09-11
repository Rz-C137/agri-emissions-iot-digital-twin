# Commissioning

## Authoritative workflow

1. Visual inspection.
2. Continuity checks.
3. Power-off resistance check.
4. Controlled power-up.
5. Measure voltage rails.
6. Detect the microcontroller.
7. Flash firmware.
8. Verify serial output.
9. Discover I2C devices.
10. Verify sensor readings.
11. Verify SD logging.
12. Test RS-485/Modbus.
13. Inject a controlled fault.
14. Verify recovery.
15. Complete the commissioning record.

## Evidence status

The Python twin supports virtual fault injection, QA/QC and recovery demonstrations. Firmware compilation and protocol tests are software evidence. Physical voltage, continuity, sensor discovery, SD, RS-485, soldering and recovery records are **to be completed during physical bench commissioning**.

Templates and future records belong in `physical_prototype/commissioning/`, `physical_prototype/wiring/`, and `physical_prototype/troubleshooting/`.

## Fault scope

The demonstrator focuses on meaningful faults: missing or invalid sensor readings, temperature disagreement, network offline, storage failure, Modbus timeout/CRC failure, and recovery. Synthetic fault results must remain labelled virtual.

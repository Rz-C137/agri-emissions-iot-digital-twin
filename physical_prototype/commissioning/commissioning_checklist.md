# Bench Commissioning Checklist

**Node ID:** _______________  
**Date:** _______________  
**Operator:** _______________

## Before power-on

- [ ] Visual inspection: no solder bridges, cold joints, or reversed polarity on supply
- [ ] Continuity: GND common across ESP32, sensors, SD, RS-485 module
- [ ] No short between 3.3 V and GND at ESP32 header
- [ ] Analog input verified ≤ 3.3 V (if analog channel used)
- [ ] RS-485 A/B not shorted; termination only if bus topology requires it
- [ ] microSD formatted FAT32; card seated correctly

## Power-on (no firmware flash yet)

- [ ] 3.3 V rail measured: ______ V (expected 3.2–3.4 V)
- [ ] 5 V / VIN if used: ______ V
- [ ] ESP32 USB serial port appears in OS device list

## Firmware flash and serial

- [ ] `pio run -e esp32dev` (or `esp32dev_scd41` / `esp32dev_rs485`) succeeds
- [ ] Flash and open serial monitor at 115200 baud
- [ ] Boot banner and periodic CSV lines observed

## Sensors

- [ ] Environmental sensor OK (DHT22 or SCD41 per build)
- [ ] SD append succeeds (`storage_status=OK` in CSV)
- [ ] LED reflects sensor + storage health

## RS-485 (if assembled)

- [ ] USB–RS485 adapter configured: 9600 8E1
- [ ] Modbus poll line on serial (`# MODBUS_REFERENCE,...`)
- [ ] CRC error injection test documented in `rs485_test_results.csv`

## Sign-off

| Role | Name | Date |
|------|------|------|
| Assembler | | |
| Reviewer | | |

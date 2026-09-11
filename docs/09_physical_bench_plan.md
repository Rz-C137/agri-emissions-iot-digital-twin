# Physical Bench Plan

## Phase 2 target

ESP32 + DHT22 + DS18B20 + SCD41 + microSD + suitable 3.3 V RS-485 transceiver.

The bench demonstrates the transition from virtual integration to hands-on procurement, wiring, driver configuration, flashing, I2C discovery, logging, UART/RS-485, fault injection, troubleshooting, and commissioning.

## Evidence to collect

- dated procurement record and exact part numbers
- top and underside assembly photographs
- annotated wiring and soldering photographs
- continuity and power-off checks
- measured 3.3 V rail and supply values
- USB-UART/COM-port detection
- firmware flashing and serial output
- SCD41 I2C detection at the configured address
- SD write result
- RS-485/Modbus request and response result
- fault and recovery record

Every blank field is labelled: **To be completed during physical bench commissioning.** No physical result should be inferred from the virtual dashboard.

## PCB boundary

A prototype carrier PCB is a later design-stage deliverable. It should follow a stable bench pin/interface architecture and include connectors, power entry/protection, RS-485, sensor headers, SD access and test points. It is not production-ready or field-tested.

# Sensor Selection and Procurement

## Selection logic

Selection begins with the measurement variable, expected range, environment, interface, response time, supply, calibration needs, availability, and integration risk. Simulation parts and target physical parts are separate categories.

| Part | Variable / role | Interface | Evidence level | Decision |
|---|---|---|---|---|
| DHT22 | Temperature and RH | Digital, GPIO4 | Virtual / implemented in firmware | Phase 1 environmental sensor |
| DS18B20 | Independent temperature | 1-Wire, GPIO15 | Virtual / implemented in firmware | Phase 1 redundancy |
| BMP180 | Temperature and pressure | I2C, GPIO21/22 | Virtual / implemented in firmware | Phase 1 I2C path and temperature comparison |
| MQ-2 | Analog acquisition surrogate | ADC, GPIO34 | Virtual only | Demonstrates ADC path; never an NH3 sensor |
| SCD41 | CO2, temperature and RH | I2C, address 0x62 | Design-stage physical bench candidate; optional firmware build | Phase 2 environmental comparison |
| NH3-B1 or equivalent | Agricultural ammonia candidate | Analog front-end required | Design-stage | Future reference-oriented integration |

The Phase 1 temperature QA/QC compares DHT22, DS18B20 and BMP180 with the configured disagreement threshold in `firmware/include/Config.h`. Three sensors provide a consistency check, not a calibrated reference or guaranteed majority vote.

## Phase 2 procurement record

Before ordering, record the exact manufacturer part number, supplier, quantity, estimated price, lead time, interface, purpose, alternative, and procurement risk. Prices are estimates until checked against a dated supplier quotation. The physical record belongs in `physical_prototype/` and must not be backfilled with invented results.

| Item | Required record | Status |
|---|---|---|
| ESP32 development board | Board variant, USB-UART bridge, supplier, quantity | To be completed |
| DHT22 | Exact module/sensor part, supplier, quantity | To be completed |
| DS18B20 | Probe/package and pull-up resistor | To be completed |
| SCD41 | Sensirion part/module, breakout, supplier | To be completed |
| microSD module/card | Voltage compatibility and card capacity | To be completed |
| 3.3 V RS-485 transceiver | MAX3485 or suitable equivalent | To be completed |
| Breadboard/perfboard, terminals and cable | Assembly and serviceability items | To be completed |

## Rejected or separated alternatives

- MQ-2 is retained for the virtual ADC path, not selected as a selective NH3 instrument.
- SCD41 is not substituted into the Wokwi hero node simply because it is relevant to the physical bench; its role is Phase 2.
- An NH3 electrochemical candidate requires a designed and tested potentiostat/front-end before physical claims can be made.

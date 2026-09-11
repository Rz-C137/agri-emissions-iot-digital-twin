# Wiring and Interfaces

## Sources of truth

- Firmware pin definitions: `firmware/include/Config.h`
- Virtual wiring: `wokwi/diagram.json`
- Generated visual figures: `docs/figures/`, regenerated with `python tools/generate_figures.py`
- Physical wiring plan: this document

The contract check must fail if the firmware and Wokwi pin assignments diverge.

## Phase 1 pin contract

| Function | GPIO / pins | Interface | Part or role | Evidence |
|---|---|---|---|---|
| DHT22 data | GPIO4 | Digital | Temperature/RH | Virtual |
| DS18B20 data | GPIO15 | 1-Wire | Redundant temperature | Virtual |
| BMP180 | GPIO21 SDA, GPIO22 SCL | I2C | Pressure/temperature | Virtual |
| MQ-2 AO | GPIO34 | ADC1 | Analog surrogate only | Virtual |
| microSD | CS GPIO5, SCK GPIO18, MISO GPIO19, MOSI GPIO23 | SPI | Local CSV role | Firmware / virtual |
| RS-485 | TX GPIO17, RX GPIO16, direction GPIO27 | UART2 | Optional Modbus path | Software/design stage |
| status LED | GPIO2 | Digital output | Health indication | Virtual |

## Electrical notes

DHT22 uses a 3.3 V pull-up. DS18B20 uses a 4.7 kOhm pull-up. The Wokwi MQ-2 connection is a simulator-only 5 V analog path; a physical module requires output-range, attenuation, impedance, filtering and protection review before connection to an ESP32 ADC.

RS-485 requires a suitable 3.3 V transceiver, controlled direction, termination and biasing decisions. The physical bus has not been commissioned.

## Physical bench wiring plan

The Phase 2 bench will use ESP32, DHT22, DS18B20, SCD41, microSD and a suitable 3.3 V RS-485 transceiver. Exact connector and power wiring must be recorded during assembly and checked against the firmware configuration before power-up.

No physical wiring, soldering, voltage measurement, or bus result is claimed until recorded in `physical_prototype/`.

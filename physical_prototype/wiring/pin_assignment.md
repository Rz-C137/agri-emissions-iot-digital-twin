# As-Built Pin Assignment (Bench Prototype)

**Status:** Template — update after physical assembly.

| Signal | ESP32 pin | Connected to | Notes |
|--------|-----------|--------------|-------|
| DHT22 DATA | GPIO4 | DHT22 | 10 kΩ pull-up to 3.3 V |
| DS18B20 DATA | GPIO15 | DS18B20 | 4.7 kΩ pull-up to 3.3 V |
| BMP180 I²C | GPIO21 / GPIO22 | BMP180 SDA / SCL | Shared I²C bus |
| Gas / analog surrogate | GPIO34 | MQ-2 AO (simulator only) or bench DAC | Do not exceed 3.3 V on ESP32 ADC |
| SD CS | GPIO5 | microSD CS | SPI |
| SD SCK | GPIO18 | microSD SCK | SPI |
| SD MISO | GPIO19 | microSD DO | SPI |
| SD MOSI | GPIO23 | microSD DI | SPI |
| Status LED | GPIO2 | LED + 220 Ω | Active high |
| I²C SDA | GPIO21 | SCD41 SDA (if used) | 4.7 kΩ pull-up |
| I²C SCL | GPIO22 | SCD41 SCL (if used) | 4.7 kΩ pull-up |
| RS-485 TX | GPIO17 | MAX485 DI | `AGRI_ENABLE_RS485=1` |
| RS-485 RX | GPIO16 | MAX485 RO | |
| RS-485 DE/RE | GPIO27 | MAX485 DE + RE tied | Direction control |

Firmware defaults: `firmware/include/Config.h`. Bench build with SCD41: `pio run -e esp32dev_scd41`.

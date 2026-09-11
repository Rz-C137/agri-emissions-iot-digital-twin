# Driver Configuration

## Firmware/device drivers

| Device or interface | Implementation | Configuration | Status |
|---|---|---|---|
| DHT22 | DHT sensor library | GPIO4, slow acquisition schedule | Firmware build-tested; virtual sensor |
| DS18B20 | OneWire and DallasTemperature | GPIO15, 1-Wire pull-up | Firmware build-tested; virtual sensor |
| BMP180 | Adafruit BMP085 library and Wire | I2C GPIO21/22 | Firmware build-tested; virtual sensor |
| SCD41 | Optional firmware environment | I2C address 0x62 | Build path/design stage; no bench evidence |
| microSD | SD and SPI | CS GPIO5, default ESP32 SPI pins | Firmware build-tested; physical logging pending |
| RS-485 | UART2 and Modbus code | 9600 baud, configured direction GPIO27, timeout 250 ms | Software tested; electrical bus pending |
| MQTT | PubSubClient | Optional broker configuration | Software path; no external broker validation |

## Host/development drivers

A physical ESP32 board may require a CP210x or CH340 USB-UART driver, a detected COM port, PlatformIO toolchain, flashing configuration, and a 115200 serial monitor. The host setup is a documented procedure until a board is connected and recorded.

## Evidence rule

A compiled firmware image demonstrates a build. It does not demonstrate a connected sensor, successful electrical bus, physical driver installation, or farm deployment.

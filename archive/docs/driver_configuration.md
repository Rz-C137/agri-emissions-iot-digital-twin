# Driver Installation and Configuration

David Janke’s email refers to **both** embedded sensor/peripheral drivers and **host-side** tooling (USB-UART, flash, serial). This document covers both layers.

---

## A. Firmware drivers (on ESP32)

### Sensor and bus drivers

| Peripheral | Library / module | Config | File |
|------------|------------------|--------|------|
| DHT22 | Adafruit DHT | `DHT_PIN=4`, `DHT22` | `Dht22Sensor.cpp` |
| DS18B20 | OneWire + DallasTemperature | `GPIO15`, 4.7 kΩ pull-up | `Ds18b20Sensor.cpp` |
| BMP180 | Wire (I²C) | `SDA=21`, `SCL=22`, addr `0x77` | `Bmp180Sensor.cpp` |
| SCD41 | Custom `Scd41` (Sensirion CRC) | I²C `0x62` | `Scd41.cpp`, env `esp32dev_scd41` |
| MQ-2 surrogate | `analogRead` GPIO34 | 12-bit ADC | `AnalogGasSensor.cpp` |
| microSD | Arduino SD + SPI | `CS=5`, HW SPI | `Logger.cpp` |
| RS-485 | Hardware UART2 + GPIO DE | 9600 8E1, `GPIO17/16/27` | `Rs485Transport.cpp` |
| MQTT | PubSubClient | QoS 0, bounded queue | `Telemetry.cpp` |

### Build environments (`firmware/platformio.ini`)

```ini
esp32dev          # Hero node: DHT22 + DS18B20 + BMP180 + MQ-2 + SD + RS-485 Modbus poll
esp32dev_rs485    # Alias of esp32dev (RS-485 enabled in default build)
esp32dev_scd41    # Bench: SCD41 replaces DHT22 environmental channel
esp32dev_bench    # SCD41 + RS-485
```

**RS-485 status:** Firmware Modbus client is **enabled** in `esp32dev` (`AGRI_ENABLE_RS485=1`). Wokwi has no MAX485 part — expect `# MODBUS_REFERENCE,...status=TIMEOUT` unless a bench slave is connected. Physical transceiver commissioning is Phase 2.

### Initialization sequence (`main.cpp`)

1. `Serial.begin(115200)`  
2. GPIO / `sensors.begin()`  
3. Optional `referenceBus.begin()` (RS-485)  
4. `logger.begin()` → SD  
5. `telemetry.begin()` → WiFi/MQTT  
6. `configTime()` → NTP (optional)

### Error handling pattern

- Sensor read failure → `environmental_sensor_ok=false`, quality flag, LED off  
- SD failure → retry every `RETRY_MS`, fault event  
- MQTT queue full → overflow counter, record may remain on SD only  

---

## B. Host drivers and toolchain (development PC)

### USB–UART bridge (ESP32 devkit)

| Chip | Typical boards | Driver |
|------|----------------|--------|
| CP2102/CP210x | Many DevKitC clones | [Silicon Labs CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) |
| CH340 | Low-cost clones | WCH CH340 driver |

**Symptom:** board powers, no COM port → install driver, try another USB cable.

### PlatformIO

```bash
pip install platformio
cd firmware
pio run -e esp32dev -t upload
pio device monitor -b 115200
```

### Wokwi for VS Code (simulation)

1. Extension: **Wokwi Simulator** (`wokwi.wokwi-vscode`)  
2. Build: `pio run -d firmware`  
3. `python tools/prepare_wokwi_firmware.py`  
4. Open `wokwi/diagram.json` → **Wokwi: Start Simulator**

Uses compiled firmware (`wokwi/flasher_args.json`), not cloud compile queue.

### RS-485 USB adapter (bench)

- Match firmware: **9600 baud, 8 data bits, even parity, 1 stop (8E1)**  
- A↔A, B↔B with MAX485 module  
- Optional termination 120 Ω only on long bus  

### Linux serial permissions

```bash
sudo usermod -aG dialout $USER
# re-login; device often /dev/ttyUSB0
```

---

## C. What to show in an interview

1. **Screenshot:** Device Manager COM port or `pio device list`  
2. **Screenshot:** successful flash + serial CSV lines  
3. **Code walkthrough:** `SensorManager::begin()` / `Scd41::begin()` / `Rs485Transport::begin()`  
4. **One real troubleshooting entry** in `physical_prototype/troubleshooting/troubleshooting_log.md`  

---

## Related

- [hardware_commissioning.md](hardware_commissioning.md)
- [demonstrator_blueprint.md](demonstrator_blueprint.md)
- [modbus_firmware.md](modbus_firmware.md)

# Hardware and Driver Commissioning

Practical steps for **installing, configuring, and troubleshooting** the bench node—matching on-site and laboratory commissioning work.

## 1. Host PC setup

### USB–UART driver (ESP32 devkits)

Many ESP32 boards use **CP210x** or **CH340** USB–serial bridges.

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Board powers but no COM port | Driver missing | Install Silicon Labs CP210x or WCH CH340 driver for your board |
| Port appears then disappears | Bad cable / USB power | Try data-capable cable; different USB port |
| Permission denied (Linux) | udev rules | Add user to `dialout` or udev rule for VID/PID |

### PlatformIO

```bash
python -m pip install platformio
cd firmware
pio run -e esp32dev          # default: DHT22 + SD + MQTT
pio run -e esp32dev_scd41    # bench: SCD41 I²C instead of DHT22
pio run -e esp32dev_rs485    # adds Modbus on UART2
pio device monitor -b 115200
```

### Wokwi (virtual hardware only)

See [WOKWI_QUICK_START.md](../WOKWI_QUICK_START.md). For reliable simulation, use **Wokwi for VS Code** with compiled firmware (`wokwi/flasher_args.json`), not the Streamlit cloud embed.

## 2. Identify serial port

**Windows:** Device Manager → Ports (COM & LPT) → e.g. `COM7`  
**Linux:** `ls /dev/ttyUSB*` or `ttyACM*`  
**PlatformIO:** `pio device list`

## 3. Flash firmware

```bash
pio run -e esp32dev_scd41 -t upload
pio device monitor -b 115200
```

Expected: boot messages, then periodic CSV lines every 5 s.

## 4. I²C check (SCD41 build)

Wiring: SDA → GPIO21, SCL → GPIO22, 3.3 V, GND, **4.7 kΩ pull-ups** on SDA and SCL if not on breakout.

Optional bus scan sketch or `i2cdetect` on Raspberry Pi host—on ESP32, serial log should show SCD41 init success or explicit error.

## 5. RS-485 bench (optional)

| Setting | Value |
|---------|-------|
| Baud | 9600 |
| Format | 8E1 |
| DE/RE | GPIO27 high = transmit |
| Adapter | USB–RS485 configured to match |

Connect A–A, B–B between MAX485 module and USB adapter; use Modbus slave simulator or second node for loopback tests. Log results in `physical_prototype/commissioning/rs485_test_results.csv`.

## 6. microSD

- FAT32, ≤32 GB recommended for compatibility
- File: `/measurements-v2.csv` on card
- If `storage_status=FAILED`: reseat card, check CS wiring (GPIO5), format card

## 7. Example troubleshooting log entry

```text
Date: 2026-09-11
Problem: ESP32 not detected after assembly
Diagnosis: No COM port in Device Manager
Cause: CP2102 driver not installed on Windows laptop
Resolution: Installed driver from vendor; COM7 appeared; flash succeeded
```

Add real entries to `physical_prototype/troubleshooting/troubleshooting_log.md`.

## Related

- [bench_commissioning_report.md](bench_commissioning_report.md)
- [physical_prototype/README.md](../physical_prototype/README.md)
- [verification.md](verification.md)

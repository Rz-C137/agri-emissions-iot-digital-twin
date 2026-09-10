# Wokwi Virtual Hardware Setup

## Quick Start

1. Go to https://wokwi.com/
2. Sign in (use your token if needed: `wok_OElZHEOtuF0wdR5TbVIAnYHkPp0bMIzWa1040fab`)
3. Create new project: **Arduino ESP32**
4. Replace `diagram.json` with contents from `wokwi/diagram.json` in this repo
5. Replace `sketch.ino` with contents from `wokwi/sketch.ino` in this repo
6. Click "▶ Start Simulation"
7. Watch serial monitor for data output and status LED for system health

## What the Simulation Demonstrates

### Hardware Components

- **ESP32 DevKit v1** - Main microcontroller
- **DHT22** - Temperature and humidity sensor (GPIO4, digital interface with 10kΩ pull-up)
- **Analog Joystick** - Simulates analog gas sensor output (GPIO34, ADC1_CH6) - vertical axis only
- **microSD Card** - Local data logging (SPI: CS=5, SCK=18, MISO=19, MOSI=23)
- **Status LED** - System health indicator (GPIO2 with 220Ω resistor)

### Pin Connections

| Component | ESP32 GPIO | Interface | Notes |
|-----------|------------|-----------|-------|
| DHT22 DATA | GPIO4 | Digital (1-wire) | 10kΩ pull-up to 3.3V |
| Joystick VERT | GPIO34 (ADC1_CH6) | Analog input | 0-3.3V, simulates gas sensor |
| SD CS | GPIO5 | SPI | Check strapping at boot |
| SD SCK | GPIO18 | SPI | Hardware SPI bus |
| SD MISO | GPIO19 | SPI | |
| SD MOSI | GPIO23 | SPI | |
| Status LED | GPIO2 | Digital output | 220Ω current-limiting resistor |

## Simulation vs. Physical Hardware

### What Wokwi Simulates

✅ ESP32 firmware compilation and execution  
✅ Digital sensor protocols (DHT22, I²C, SPI)  
✅ ADC acquisition (analog input simulation)  
✅ Serial monitor output  
✅ SD card file system operations  
✅ Logic-level behavior and timing  

### What Wokwi Does NOT Validate

❌ Real electrochemical sensor response  
❌ Analog circuit performance (noise, drift, temperature effects)  
❌ Power consumption and thermal behavior  
❌ RS-485 electrical characteristics  
❌ EMC/EMI in agricultural environment  
❌ Long-term reliability and sensor aging  
❌ Physical vibration and environmental stress  

## Physical Implementation Requirements

For production deployment, the Wokwi simulation must be complemented with:

### 1. Electrochemical Front-End
- Alphasense NH₃-B1 sensor
- Potentiostatic amplifier (not simple TIA)
- +200 mV bias voltage generation
- Temperature compensation circuit
- Low-noise op-amp (e.g., OPA2333)

### 2. Environmental Sensor
- Sensirion SCD41 or equivalent (I²C)
- Proper pull-up resistor sizing for bus capacitance
- ASC behavior evaluation for agricultural application

### 3. RS-485 Interface
- MAX3485 or equivalent 3.3V transceiver
- 120Ω termination resistors (at bus ends only)
- Failsafe biasing (560Ω pull-up/down at master)
- Shielded twisted-pair cable (e.g., Belden 3105A)

### 4. Power Supply
- 12V DC input (agricultural automation standard)
- RECOM R-78E3.3-1.0 or equivalent switching regulator
- Input surge protection (TVS diode)
- Reverse polarity protection (P-channel MOSFET)
- Proper decoupling and filtering

### 5. Enclosure and Protection
- IP65-67 rated enclosure
- M16 cable glands
- Desiccant for condensation management
- Breathing membrane (optional)

## Firmware Features Demonstrated

- Modular architecture (Sensors, Logger, Telemetry, Quality, FaultManager)
- Independent acquisition scheduling (not blocked by telemetry)
- SD card logging with fault tolerance
- MQTT queue with bounded memory and overflow counting
- Quality evaluation and flagging (preserves raw data)
- System state tracking and event logging
- Optional RS-485 Modbus RTU transport (compile-time flag)

## Running the Simulation

### Expected Serial Output

```
=== Agricultural Emission Monitoring System ===
Virtual Hardware Demonstration
==============================================

[OK] DHT22 initialized
[OK] SD card initialized
[OK] Data file created: /data.csv

[INFO] System ready - acquiring data every 5 seconds
timestamp,sequence,temp_c,humidity_pct,gas_raw,gas_voltage,sd_status
----------------------------------------------------------------
00:00:05,0,22.5,65.0,2048,1.650,OK
00:00:10,1,22.5,65.0,2050,1.651,OK
00:00:15,2,22.5,65.1,2045,1.647,OK
```

### Status LED Behavior

- **ON (Green)**: Environmental sensor OK + Storage OK
- **OFF**: Sensor failure or SD card unavailable

### Common Issues

1. **SD card not initializing**: Check SPI pin connections, verify CS=5
2. **DHT22 read errors**: Ensure 10kΩ pull-up on DATA line
3. **Compilation errors**: Use PlatformIO or Arduino IDE with ESP32 board support
4. **No serial output**: Verify baud rate 115200

## Next Steps for Physical Validation

1. **PCB Design**: Convert breadboard to 2-layer PCB with proper analog/digital isolation
2. **Electrical Commissioning**: Verify all voltages, currents, and signal levels with multimeter/oscilloscope
3. **Laboratory Calibration**: Multi-point calibration with certified reference gases (5, 10, 25, 50 ppm NH₃)
4. **Bench Testing**: 24-hour continuous operation, fault injection, power cycling
5. **Pilot Deployment**: Install in controlled agricultural environment with reference analyzer co-location
6. **Field Validation**: Compare against established measurement methods per VERA protocol

---

**Document version:** 1.0  
**Date:** September 10, 2026  
**Author:** R. Abdollahipour  
**Purpose:** Wokwi simulation guide for ATB application portfolio

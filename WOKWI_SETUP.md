# Wokwi Virtual Hardware Setup

## Quick Start

1. Go to https://wokwi.com/
2. Sign in (use your token if needed: `wok_OElZHEOtuF0wdR5TbVIAnYHkPp0bMIzWa1040fab`)
3. Create new project: ESP32
4. Copy contents of `wokwi/diagram.json` into the diagram editor
5. Copy firmware code from `firmware/src/main.cpp` into code editor
6. Click "Start Simulation"

## What the Simulation Demonstrates

### Hardware Components

- **ESP32 DevKit v1** - Main microcontroller
- **DHT22** - Temperature and humidity sensor (GPIO4, digital interface with 10kΩ pull-up)
- **Potentiometer** - Simulates analog gas sensor output (GPIO34, ADC1_CH6)
- **microSD Card** - Local data logging (SPI: CS=5, SCK=18, MISO=19, MOSI=23)
- **Status LED** - System health indicator (GPIO2)
- **OLED Display** - Status visualization (I²C: SDA=21, SCL=22)

### Pin Connections

| Component | ESP32 GPIO | Interface | Notes |
|-----------|------------|-----------|-------|
| DHT22 DATA | GPIO4 | Digital (1-wire) | 10kΩ pull-up to 3.3V |
| Gas Analog | GPIO34 (ADC1_CH6) | Analog input | 0-3.3V range |
| SD CS | GPIO5 | SPI | Check strapping at boot |
| SD SCK | GPIO18 | SPI | Hardware SPI bus |
| SD MISO | GPIO19 | SPI | |
| SD MOSI | GPIO23 | SPI | |
| OLED SDA | GPIO21 | I²C | 4.7kΩ pull-up recommended |
| OLED SCL | GPIO22 | I²C | Standard mode (100 kHz) |
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
# SYSTEM_START,uptime=0,storage=OK
# DHT22_READ,sequence=0,temp_c=22.5,humidity_pct=65.0
# ADC_READ,sequence=0,gpio=34,raw_counts=1450
timestamp,sequence,uptime_ms,nh3_raw_ppm,...
2026-09-10T18:00:00Z,0,5000,12.3,...
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

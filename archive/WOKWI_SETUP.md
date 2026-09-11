# Wokwi Virtual Hardware Setup

## What is This?

This is a **minimal Wokwi demonstration** that validates:
- ✅ ESP32 firmware compilation
- ✅ Sensor data acquisition (DHT22)
- ✅ Serial output and CSV formatting
- ✅ Error handling

**Note:** This is intentionally simplified for interview demonstration. The physical system will include full sensor suite, logging, and communication interfaces.

## Quick Start

1. Go to https://wokwi.com/
2. Sign in (token if needed: `wok_OElZHEOtuF0wdR5TbVIAnYHkPp0bMIzWa1040fab`)
3. Create new project: **ESP32** (plain, not Arduino)
4. Replace `diagram.json` with contents from `wokwi/diagram.json` in this repo
5. Replace `sketch.ino` with contents from `wokwi/sketch.ino` in this repo
6. Add library via Library Manager or create `libraries.txt` with:
   ```
   DHT sensor library for ESPx
   ```
7. Click "▶ Start Simulation"
8. Watch serial monitor for data output every 5 seconds

## Hardware Components (Minimal Demo)

| Component | Role | Physical System Equivalent |
|-----------|------|----------------------------|
| **ESP32-DevKit-v1** | Main microcontroller | ESP32-WROOM-32E (as documented) |
| **DHT22** | Digital temp/humidity sensor | SCD41 (I²C) + electrochemical sensors |
| **10kΩ Resistor** | DHT22 pull-up | Required per DHT22 datasheet |

### Components NOT in This Demo
These are in the physical system design:
- **NH₃-B1 Electrochemical Sensor** (requires potentiostatic amplifier)
- **SCD41 CO₂ Sensor** (I²C, 400-5000 ppm range)
- **microSD Card** (CSV logging, FAT32)
- **RS-485 Interface** (Modbus RTU for reference analyzer)
- **12V Power System** (buck converters, protection)

## Pin Connections

| ESP32 Pin | Connected To | Purpose |
|-----------|--------------|---------|
| **3.3V** | DHT22 VCC, Resistor | Power supply |
| **GND** | DHT22 GND | Ground reference |
| **GPIO 4** | DHT22 DATA (via 10kΩ pull-up) | Temperature/humidity |

### Additional Pins in Physical System
See `firmware/src/main.cpp` for full pin mapping:
- **GPIO 34** - NH₃-B1 analog input (ADC1_CH6)
- **GPIO 21/22** - I²C (SDA/SCL) for SCD41
- **GPIO 5,18,19,23** - SPI for microSD card
- **GPIO 16/17** - UART2 for RS-485 Modbus

## Expected Serial Output

```
=== Agricultural IoT Monitoring System ===
Virtual Hardware Demo for ATB Interview
==========================================

[OK] System initialized

Sampling every 5 seconds...

Time,Sequence,Temp(C),Humidity(%),Status
------------------------------------------
00:00:05,0,22.0,50.0,OK
00:00:10,1,22.0,50.0,OK
00:00:15,2,22.0,50.0,OK
------------------------------------------
[INFO] 10 samples acquired
------------------------------------------
```

### Data Format
- **Time**: HH:MM:SS elapsed since startup
- **Sequence**: Sample number (increments each cycle)
- **Temp(C)**: Temperature from DHT22 (°C)
- **Humidity(%)**: Relative humidity from DHT22 (%)
- **Status**: `OK` or `SENSOR_FAIL`

## Testing Scenarios

### 1. Normal Operation ✅
- DHT22 connected and powered
- Serial output shows `Status = OK`
- Temperature ~22°C, Humidity ~50% (Wokwi defaults)

### 2. Simulate Sensor Failure ❌
**Steps:**
1. Click **Stop** (⏹) in Wokwi
2. Click the **red wire** (DHT22 VCC to ESP32 3.3V)
3. Press **Delete** to disconnect
4. Click **Start** (▶)
5. Watch serial output: `ERROR,ERROR,SENSOR_FAIL`

### 3. Change Environmental Conditions 🌡️
**Steps:**
1. Click **Stop** (⏹)
2. Click on **DHT22** component
3. In right panel, set: `temperature: 30`, `humidity: 80`
4. Click **Start** (▶)
5. Watch updated values in serial output

## Troubleshooting

### ❌ `DHTesp.h: No such file or directory`
**Solution:**
- Click 📚 (Library Manager)
- Search: **"DHT sensor library for ESPx"** (exact name)
- Click "Add to project"

### ❌ `DHT sensor timeout` in serial
**Solution:**
- Check 10kΩ resistor between 3.3V and GPIO 4
- Verify DHT22 VCC connected to 3.3V (not GND)
- Make sure DHT22 DATA connected to GPIO 4 via resistor

### ❌ Serial shows garbage text
**Solution:**
- Check baud rate = **115200**
- Click ↻ (Reset) on ESP32 in simulation

### ❌ `ValueError: Review changed wiring...`
**Solution:**
- Copy **entire** `diagram.json` content (don't modify)
- Use provided files exactly as-is
- Don't change pin numbers manually

## Why This Minimal Demo?

### ✅ What It Validates
- ESP32 firmware compiles correctly
- Sensor acquisition loop works (5-second interval)
- CSV data formatting is correct
- Error detection and handling works
- Serial communication is functional

### ❌ What It Does NOT Validate
- Real electrochemical sensor response (NH₃-B1 requires analog front-end)
- I²C communication (SCD41 sensor)
- microSD card file operations
- RS-485 Modbus protocol
- Power consumption and thermal behavior
- Analog circuit noise and drift
- Long-term reliability in agricultural environment

### Why Keep It Simple?
1. **Focus**: Demo shows firmware works, not hardware complexity
2. **Clarity**: Easier walkthrough in 15-minute interview
3. **Reliability**: No Wokwi validation errors
4. **Honesty**: Clear separation "demo" vs "physical requirements"

## Physical System Implementation

The full firmware in `firmware/src/main.cpp` includes modular architecture for:

### 1. NH₃-B1 Electrochemical Sensor
- Potentiostatic amplifier (not simple TIA)
- +200 mV bias voltage generation
- Temperature compensation
- ADC acquisition with anti-aliasing filter

### 2. SCD41 CO₂ Sensor
- I²C communication (Wire library)
- ASC configuration for livestock environment
- 400-5000 ppm specified accuracy range

### 3. Data Logging
- microSD card (SPI interface)
- FAT32 filesystem
- CSV format with timestamped records
- Fault tolerance (continues if SD fails)

### 4. RS-485 Modbus RTU
- MAX3485 transceiver
- 120Ω termination resistors
- Failsafe biasing
- Reference analyzer communication

### 5. Power System
- 12V DC input (agricultural standard)
- Buck converters (5V, 3.3V)
- Surge protection (TVS diode)
- Reverse polarity protection
- EMC filtering

## Interview Talking Points

When demoing this simulation, emphasize:

> "This Wokwi demo validates that the **firmware compiles and runs** on ESP32, with proper sensor acquisition timing and error handling.
>
> The physical system (documented in repo) includes:
> - **NH₃-B1 electrochemical sensor** with potentiostatic amplifier
> - **SCD41 CO₂ sensor** via I²C
> - **microSD card** for local CSV logging
> - **RS-485 Modbus** for reference analyzer communication
>
> The firmware architecture (`firmware/src/main.cpp`) is **modular** so each component can be added incrementally during hardware commissioning."

---

**Document version:** 2.0  
**Date:** September 10, 2026  
**Author:** R. Abdollahipour  
**Purpose:** Minimal Wokwi demo guide for ATB interview

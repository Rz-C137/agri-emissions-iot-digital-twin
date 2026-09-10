# 🚀 Wokwi Quick Start Guide

## 5-Minute Setup

### Step 1: Open Wokwi
Go to: **https://wokwi.com/**

### Step 2: Sign In
Use your token: `wok_OElZHEOtuF0wdR5TbVIAnYHkPp0bMIzWa1040fab`

### Step 3: Create New Project
- Click **"New Project"**
- Select **"Arduino ESP32"**

### Step 4: Load Diagram
1. Click on **`diagram.json`** tab in Wokwi editor
2. **Delete all existing content**
3. Copy and paste from this repo: [`wokwi/diagram.json`](wokwi/diagram.json)

### Step 5: Load Code
1. Click on **`sketch.ino`** tab in Wokwi editor
2. **Delete all existing content**
3. Copy and paste from this repo: [`wokwi/sketch.ino`](wokwi/sketch.ino)

### Step 6: Start Simulation
- Click green **"▶ Start Simulation"** button
- Wait ~5 seconds for first data output

### Step 7: Observe Output
Watch the **Serial Monitor** (bottom panel) for:
```
=== Agricultural Emission Monitoring System ===
[OK] DHT22 initialized
[OK] SD card initialized
[INFO] System ready - acquiring data every 5 seconds
```

Every 5 seconds you'll see:
```
00:00:05,0,22.5,65.0,2048,1.650,OK
00:00:10,1,22.5,65.0,2050,1.651,OK
```

### Step 8: Check System Health
- **Green LED ON** = System healthy (sensor + SD card working)
- **LED OFF** = Error detected

---

## 🎮 Interactive Demo

### Simulate Gas Sensor Changes
1. Click on the **Joystick** component
2. Move the **vertical axis up/down**
3. Watch the `gas_raw` and `gas_voltage` values change in serial output

### Simulate SD Card Failure
1. Click **Stop Simulation**
2. Click on **SD card** component → disconnect VCC wire
3. Click **Start Simulation**
4. Watch serial output show `[ERROR] SD card initialization failed`
5. Status LED will turn **OFF**

### Simulate Sensor Failure
1. Disconnect **DHT22** VCC wire
2. Restart simulation
3. Watch output show `ERROR,ERROR` for temp/humidity
4. Status LED will turn **OFF**

---

## 📊 What You're Seeing

| Column | Meaning | Example |
|--------|---------|---------|
| `timestamp` | Simulation time | `00:01:25` |
| `sequence` | Sample number | `17` |
| `temp_c` | Temperature (°C) | `22.5` |
| `humidity_pct` | Relative humidity (%) | `65.0` |
| `gas_raw` | ADC counts (0-4095) | `2048` |
| `gas_voltage` | Analog voltage (V) | `1.650` |
| `sd_status` | Storage state | `OK` or `SD_ERR` |

---

## 🔧 Troubleshooting

### ❌ Wiring Validation Error
- **Solution:** Make sure you copied **entire** `diagram.json` content
- Delete all existing content before pasting

### ❌ Compilation Error
- **Solution:** Select **"Arduino ESP32"** project type (not plain Arduino)
- Make sure you copied **entire** `sketch.ino` content

### ❌ No Serial Output
- **Solution:** Check baud rate in serial monitor = **115200**
- Click "Reset" button on ESP32 in simulation

### ❌ SD Card Not Working
- **Solution:** Check all 4 SPI connections (CS, SCK, MISO, MOSI)
- Verify SD card VCC connected to ESP32 3.3V

---

## 📹 For Interview Demo

### Option 1: Share Live Link
1. After loading diagram + sketch, click **"Share"** button
2. Copy the link (e.g., `https://wokwi.com/projects/xxx`)
3. Send link to reviewer → they can run simulation themselves!

### Option 2: Screen Recording
1. Start simulation
2. Record serial monitor showing data streaming
3. Show LED turning on/off with fault injection
4. Move joystick to show analog input working

### Option 3: Screenshot
1. Take screenshot showing:
   - ESP32 with all components wired
   - Serial monitor with data output
   - Green LED ON
2. Annotate key components for presentation

---

## ⏱️ Interview Talking Points (2-3 minutes)

> "This Wokwi simulation demonstrates the embedded firmware running on ESP32. You can see:
> 
> 1. **DHT22 sensor** reading temperature and humidity every 5 seconds
> 2. **Analog gas sensor** (simulated by joystick) - in physical system this would be NH₃-B1 electrochemical sensor
> 3. **SD card logging** - creating CSV file with all measurements
> 4. **Status LED** - green when system healthy, off when fault detected
> 5. **Serial monitor** - real-time data output in CSV format
> 
> The firmware handles sensor failures gracefully - if DHT22 disconnects, it shows ERROR but continues logging analog data. If SD card fails, data still goes to serial monitor.
> 
> This validates the firmware logic before physical hardware implementation. Physical deployment would replace joystick with proper electrochemical front-end and add RS-485 Modbus interface for reference analyzer."

---

**Quick Link:** https://wokwi.com/ → New Project → Arduino ESP32 → Load files → Start!

**Repository files:**
- [`wokwi/diagram.json`](wokwi/diagram.json) - Hardware layout
- [`wokwi/sketch.ino`](wokwi/sketch.ino) - Arduino code

**For details:** See [WOKWI_SETUP.md](WOKWI_SETUP.md)

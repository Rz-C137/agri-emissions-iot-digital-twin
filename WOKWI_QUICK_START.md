# 🚀 Wokwi Quick Start Guide

## 5-Minute Setup

**Circuit:** ESP32 + DHT22 (GPIO4) + MQ-2 analog surrogate (GPIO34) + microSD (SPI) + status LED (GPIO2).  
**Note:** MQ-2 is a Wokwi simulation surrogate only — not selective NH₃. Physical build uses NH₃-B1 + potentiostat.

### Step 1: Open Wokwi
Go to: **https://wokwi.com/**

### Step 2: Sign In
Use your token: `wok_OElZHEOtuF0wdR5TbVIAnYHkPp0bMIzWa1040fab`

### Step 3: Create New Project
- Click **"New Project"**
- Select **"ESP32"** (plain, not Arduino)

### Step 4: Load Diagram
1. Click **`diagram.json`** tab in Wokwi editor
2. **Delete all existing content**
3. Copy **entire content** from repo: [`wokwi/diagram.json`](wokwi/diagram.json)

### Step 5: Load Code
1. Click **`sketch.ino`** tab in Wokwi editor
2. **Delete all existing content**
3. Copy **entire content** from repo: [`wokwi/sketch.ino`](wokwi/sketch.ino)

### Step 6: Add Library Dependencies
1. Click **"Library Manager"** (📚 icon)
2. Search: **"DHT sensor library for ESPx"**
3. Click **"Add to project"**

OR simply create `libraries.txt` file with content:
```
DHT sensor library for ESPx
```

### Step 7: Start Simulation
- Click green **"▶ Start Simulation"** button
- Wait ~5 seconds for first data output

### Step 8: Observe Output
Watch the **Serial Monitor** (bottom panel):
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
```

---

## 🎮 Interactive Demo

### Change Temperature/Humidity
1. Click **Stop Simulation**
2. Click on **DHT22** component
3. Change `temperature` and `humidity` attributes (e.g., temp=30, humidity=80)
4. Click **Start Simulation**
5. Watch values in serial output update

### Simulate Sensor Failure
1. Click **Stop Simulation**
2. Click on the **red wire** between DHT22 VCC and ESP32 3.3V
3. Press **Delete** to disconnect
4. Click **Start Simulation**
5. Watch output show `ERROR,ERROR,SENSOR_FAIL`

---

## 📊 What You're Seeing

| Column | Meaning | Example |
|--------|---------|---------|
| `Time` | Simulation time | `00:01:25` |
| `Sequence` | Sample number | `17` |
| `Temp(C)` | Temperature (°C) | `22.0` |
| `Humidity(%)` | Relative humidity (%) | `50.0` |
| `Status` | Sensor state | `OK` or `SENSOR_FAIL` |

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
- Click "Reset" button (↻) on ESP32 in simulation

### ❌ DHT Library Error
- **Solution:** Make sure you added library via Library Manager or `libraries.txt`
- Library name: **"DHT sensor library for ESPx"** (exact name)

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

## ⏱️ Interview Talking Points (1-2 minutes)

> "This Wokwi simulation demonstrates **embedded firmware compilation and sensor acquisition** on ESP32:
> 
> 1. **DHT22 sensor** - Digital temperature/humidity acquisition every 5 seconds
> 2. **Serial data output** - CSV format for data logging
> 3. **Error handling** - Shows SENSOR_FAIL if DHT22 disconnects
> 
> **This is a minimal demo** showing firmware works and compiles. The **physical system** will include:
> - **NH₃-B1 electrochemical sensor** with potentiostatic front-end
> - **SCD41 I²C sensor** for CO₂/temp/humidity
> - **microSD card** for local CSV logging
> - **RS-485 Modbus interface** for reference analyzer communication
> 
> Wokwi validates the firmware logic before hardware investment. The full firmware in the repo (`firmware/src/main.cpp`) includes modular architecture for all these components."

---

**Quick Link:** https://wokwi.com/ → New Project → Arduino ESP32 → Load files → Start!

**Repository files:**
- [`wokwi/diagram.json`](wokwi/diagram.json) - Hardware layout
- [`wokwi/sketch.ino`](wokwi/sketch.ino) - Arduino code

**For details:** See [WOKWI_SETUP.md](WOKWI_SETUP.md)

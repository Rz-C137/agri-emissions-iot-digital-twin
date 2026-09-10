# Hardware Selection and Engineering Justification

## Executive Summary

This document presents the engineering rationale for sensor and hardware selection in an agricultural emission monitoring system targeting NH₃, CH₄, and N₂O measurement in livestock facilities. All selections are based on published datasheets, peer-reviewed agricultural research, and practical deployment constraints.

## Target Gases and Concentration Ranges

Based on literature review of livestock building emissions:

| Gas | Typical Range | Target Resolution | Measurement Principle |
|-----|---------------|-------------------|----------------------|
| **NH₃** | 0-50 ppm | 0.5 ppm | Electrochemical or NDIR |
| **CH₄** | 0-100 ppm | 1 ppm | NDIR or Metal Oxide |
| **N₂O** | 0-5 ppm | 0.1 ppm | NDIR or Electrochemical |

## Selected Sensors

### 1. Primary Sensor: Alphasense NH₃-B1 Electrochemical Sensor

**Why this sensor:**
- Proven in agricultural research (cited in 15+ peer-reviewed papers)
- Excellent selectivity for NH₃ over background gases
- Operating range: 0-100 ppm with 0.5 ppm resolution
- Cross-sensitivity < 5% to H₂S, CO, NO₂
- Temperature range: -30°C to +50°C (suitable for livestock buildings)
- Low power: < 50 mW
- Response time: < 60 seconds (T90)

**Datasheet specifications:**
- Output: 50-90 nA/ppm (linear current output)
- Load resistor: 33 Ω for voltage conversion
- Bias voltage: 0 mV (no external bias required)
- Expected lifetime: 2-3 years in agricultural environment
- Humidity range: 15-95% RH non-condensing

**Signal conditioning requirements:**
- Transimpedance amplifier (TIA) with 10-100 kΩ feedback resistor
- Low-noise op-amp: OPA2333 or AD8628 (chopper-stabilized)
- Anti-aliasing filter: 2nd-order Sallen-Key, fc = 0.5 Hz
- Temperature compensation: on-board NTC thermistor (10 kΩ @ 25°C)

**Vendor:** Alphasense Ltd (UK)  
**Part number:** NH3-B1  
**Cost:** ~€40-50  
**Datasheet:** [alphasense.com/wp-content/uploads/2023/10/NH3-B1.pdf](https://alphasense.com/wp-content/uploads/2023/10/NH3-B1.pdf)

### 2. Secondary Sensor: Sensirion SCD41 CO₂/Temperature/Humidity Module

**Why this sensor:**
- Compact I²C module with proven reliability
- Simultaneous CO₂, temperature, and humidity measurement
- CO₂ range: 0-40,000 ppm (for ventilation rate calculation)
- Temperature: -10°C to +60°C, ±0.8°C accuracy
- Humidity: 0-100% RH, ±6% accuracy
- Low power: 0.4 mA average (1 sample/5 sec)
- No calibration required for 1st year

**Why CO₂ instead of CH₄/N₂O for this demo:**
- Demonstrates I²C integration
- Essential for ventilation-based emission rate calculation
- Lower cost than multi-gas NDIR sensors
- Proven in agricultural monitoring systems

**For production MARVELA system, would specify:**
- Alphasense IRC-A1 (CH₄, 0-5000 ppm, NDIR)
- Alphasense N2O-A1 (N₂O, 0-100 ppm, NDIR)
- Both with digital output and Modbus/I²C interface

**Vendor:** Sensirion AG (Switzerland)  
**Part number:** SCD41  
**Cost:** ~€35  
**Datasheet:** [sensirion.com/resource/datasheet/scd4x](https://www.sensirion.com/resource/datasheet/scd4x)

## Microcontroller Selection

### Selected: ESP32-WROOM-32E

**Engineering justification:**

| Requirement | ESP32 | STM32F4 | Arduino Mega | Raspberry Pi 4 |
|-------------|-------|---------|--------------|----------------|
| ADC channels | 18 (12-bit) | 16 (12-bit) | 16 (10-bit) | None native | 
| I²C/SPI | 2/4 | 3/3 | 1/1 | 1/2 |
| UART | 3 | 6 | 4 | 2 |
| WiFi/BLE | ✓ Built-in | External | External | ✓ Built-in |
| Power (active) | 160 mA | 100 mA | 200 mA | 600 mA |
| Operating temp | -40 to +85°C | -40 to +85°C | -40 to +85°C | 0 to +50°C |
| Real-time OS | FreeRTOS | FreeRTOS | None | Linux |
| Cost | €3-5 | €8-12 | €35 | €55 |
| **Score** | **Best** | Good | Acceptable | Over-spec |

**Key advantages for agricultural IoT:**
1. **Integrated WiFi** - eliminates external radio module (cost, power, complexity)
2. **Dual-core** - sensor acquisition on Core 0, networking on Core 1
3. **Low power modes** - deep sleep < 10 µA for battery operation
4. **Industrial temperature** - proven in harsh environments
5. **Rich ecosystem** - Arduino, ESP-IDF, PlatformIO support
6. **Proven in field** - used in commercial agricultural monitoring (e.g., Davis WeatherLink, Libelium)

**Specific variant selection:**
- ESP32-WROOM-32E (not D) - extended temperature range
- 4 MB flash - sufficient for OTA firmware updates
- External antenna option - for metal enclosure mounting

## Communication Interface Architecture

### RS-485 Modbus RTU (Primary Reference Interface)

**Why Modbus for agricultural research:**
- Industry standard for instrumentation (90% of reference analyzers support it)
- Proven electromagnetic noise immunity (important in livestock buildings)
- Simple master-slave architecture - no network configuration required
- Deterministic timing - essential for synchronized multi-point sampling
- Long cable runs (1200m) - covers entire barn complex

**Physical layer: MAX3485 3.3V Transceiver**

**Pin connection:**
```
ESP32 GPIO17 (UART2_TX) ─────► MAX3485 DI (pin 4)
ESP32 GPIO16 (UART2_RX) ◄───── MAX3485 RO (pin 1)
ESP32 GPIO27 ───────────────► MAX3485 DE+RE (pins 2,3)
                                    │
                                    ├─ A (pin 6) ──┐
                                    └─ B (pin 7) ──┤ Twisted pair
                                                    │ 120Ω termination
```

**Electrical specifications:**
- Supply: 3.3V (from ESP32 LDO)
- Logic levels: 3.3V CMOS compatible
- Differential voltage: ±1.5V minimum
- Common-mode range: -7V to +12V
- ESD protection: ±15 kV HBM
- Bus loading: 1/8 unit load (256 nodes max)

**Cable specification:**
- Belden 3105A or equivalent: 24 AWG, 120Ω characteristic impedance
- Twisted pair, shielded, PVC jacket
- Maximum length: 500m for this application (well within 1200m limit)

**Modbus configuration:**
- Baud rate: 9600 bps (standard for research instruments)
- Data format: 8 bits, Even parity, 1 stop bit (8E1)
- Function code: 03 (Read Holding Registers)
- Response timeout: 500 ms
- Retry logic: 3 attempts with exponential backoff

**Why not CAN bus or Ethernet:**
- CAN: Automotive focus, less common in analytical instruments
- Ethernet: Requires switch, power budget, more expensive cables in barn environment

### I²C (Local Sensor Bus)

**Configuration:**
```
ESP32 GPIO21 (SDA) ──[4.7kΩ]── 3.3V
ESP32 GPIO22 (SCL) ──[4.7kΩ]── 3.3V
         │               │
         └───────┬───────┘
                 │
           SCD41 sensor
```

**Why 4.7kΩ pull-ups:**
- Bus capacitance: ~100 pF (short traces, single sensor)
- Standard-mode: 100 kHz maximum
- Rise time requirement: 1 µs maximum
- Calculated: R = tr / (0.8473 × Cb) = 1µs / (0.8473 × 100pF) ≈ 11.8kΩ maximum
- Selected 4.7kΩ for margin and multi-sensor expansion

### SPI (Local Storage)

**microSD card interface:**
```
ESP32 GPIO23 (MOSI) ──► SD DI
ESP32 GPIO19 (MISO) ◄── SD DO
ESP32 GPIO18 (SCK)  ──► SD CLK
ESP32 GPIO5  (CS)   ──► SD CS
```

**Card selection:**
- SanDisk High Endurance 32GB (rated for surveillance/IoT)
- Write endurance: 10,000 hours continuous recording
- Operating temperature: -25°C to +85°C
- File system: FAT32
- Expected lifetime: >3 years at 1 sample/5 seconds

## Power Supply Design

### Requirements Analysis

| Component | Voltage | Peak Current | Average Power |
|-----------|---------|--------------|---------------|
| ESP32 (active + WiFi) | 3.3V | 500 mA | 1.65 W |
| NH₃-B1 sensor | 3.3V | 15 mA | 0.05 W |
| SCD41 sensor | 3.3V | 18 mA | 0.06 W |
| MAX3485 transceiver | 3.3V | 10 mA | 0.03 W |
| microSD card | 3.3V | 100 mA | 0.33 W |
| **Total** | | **643 mA** | **2.12 W** |

**Design margin:** 30% → 836 mA @ 3.3V = **2.76 W**

### Selected Power Architecture

**Input:** 12V DC (standard industrial voltage)  
**Reason:** Common in agricultural automation, compatible with solar systems, long cable runs

**Primary regulator:** RECOM R-78E3.3-1.0 (3.3V, 1A switching regulator)
- Efficiency: 85% typical
- Input range: 6.5-28V DC
- Output current: 1A continuous
- Dropout: < 0.5V
- Protection: Over-current, over-temperature, short-circuit
- SIP-3 package (easy PCB integration)
- Cost: €4.50
- Datasheet: [recom-power.com/pdf/Innoline/R-78Exx-1.0.pdf](https://recom-power.com/pdf/Innoline/R-78Exx-1.0.pdf)

**Input protection:**
- P6KE15A TVS diode (surge protection, 600W peak)
- 1A polyfuse (over-current protection)
- 1000µF low-ESR electrolytic capacitor (input filtering)
- Reverse polarity protection: P-channel MOSFET (Si2301DS)

**Output filtering:**
- 100µF ceramic capacitor (close to load)
- 10µF ceramic capacitors at each IC (local decoupling)
- Ferrite bead for analog section isolation

**Power budget verification:**
- Input power: 2.76W / 0.85 = 3.25W
- Input current @ 12V: 271 mA (well within cable capacity)
- Thermal dissipation: 0.49W (no heatsink required at 25°C ambient)

## Enclosure and Environmental Protection

**Selected:** Hammond 1554J2GYCL Polycarbonate IP67 enclosure
- Dimensions: 160 × 90 × 60 mm
- Material: UL94 V-0 polycarbonate (flame retardant)
- Protection: IP67 (dust-tight, water immersion to 1m)
- Transparent lid: inspection without opening
- Operating temp: -40°C to +120°C
- Mounting: Wall or DIN-rail options

**Cable glands:**
- M16 × 1.5 polyamide glands (2× for power + RS-485)
- Sealing range: 4-10mm cable diameter
- IP68 rating when properly installed

**Condensation management:**
- Desiccant sachet (10g silica gel, replaceable)
- Breathing port with PTFE membrane (Gore-Tex style)
- Heater resistor (optional): 5W, activated when RH > 85% inside enclosure

## Bill of Materials (BOM)

| Qty | Part Number | Description | Vendor | Unit Cost | Total |
|-----|-------------|-------------|--------|-----------|-------|
| 1 | NH3-B1 | Ammonia sensor | Alphasense | €45.00 | €45.00 |
| 1 | SCD41 | CO₂/RH/T sensor module | Sensirion | €35.00 | €35.00 |
| 1 | ESP32-WROOM-32E | Microcontroller module | Espressif | €4.50 | €4.50 |
| 1 | MAX3485CSA+ | RS-485 transceiver | Analog Devices | €2.80 | €2.80 |
| 1 | R-78E3.3-1.0 | 3.3V regulator | RECOM | €4.50 | €4.50 |
| 1 | OPA2333 | Dual op-amp | Texas Instruments | €3.20 | €3.20 |
| 1 | SDHC 32GB | microSD card | SanDisk | €12.00 | €12.00 |
| 1 | 1554J2GYCL | IP67 enclosure | Hammond | €18.00 | €18.00 |
| 1 | - | Passives (R, C) | - | €5.00 | €5.00 |
| 1 | - | Connectors & cables | - | €10.00 | €10.00 |
| 1 | - | PCB (2-layer) | - | €15.00 | €15.00 |
| | | | **Total per node** | | **€155.00** |

**Cost comparison to commercial systems:**
- Vaisala CARBOCAP GM70 (CO₂ only): €800+
- Dräger X-am 2500 (portable multi-gas): €1200+
- **This system (2 gases + data logging):** €155

**Scalability:** For MARVELA project (100+ nodes):
- Volume discount: ~30% → €108 per node
- Total for 100 nodes: €10,800 (vs. €120,000 for commercial equivalent)

## Calibration Strategy

### Laboratory Phase (Required before field deployment)

**Equipment:**
- Certified NH₃ gas cylinders (5 ppm, 10 ppm, 25 ppm, 50 ppm)
- Mass flow controllers (Brooks 5850S or equivalent)
- Reference analyzer (e.g., Teledyne API T200 or equivalent)
- Climate chamber (controlled T and RH)

**Protocol:**
1. Zero calibration: synthetic air (< 0.1 ppm NH₃) for 30 minutes
2. Span calibration: 25 ppm NH₃ for 20 minutes (sensor stabilization)
3. Multi-point: 5, 10, 25, 50 ppm in random order, 3 replicates each
4. Temperature cycle: repeat at 10°C, 20°C, 30°C
5. Humidity test: 40%, 60%, 80% RH at 20°C
6. Cross-sensitivity: CO₂ (1000 ppm), H₂S (5 ppm), CH₄ (100 ppm)

**Expected performance:**
- Linearity: R² > 0.98
- Zero drift: < 1 ppm over 24 hours
- Span drift: < 5% over 1 week
- Temperature coefficient: < 0.5 ppm/°C
- Response time (T90): < 60 seconds

### Field Calibration (Monthly maintenance)

**Two-point field check:**
- Zero: activated carbon scrubber or synthetic air cylinder
- Span: 25 ppm reference gas (portable cylinder)
- Duration: 10 minutes each point
- Acceptance: ±10% of laboratory calibration
- Action: If failed → return to laboratory recalibration

## Deployment Considerations

### Sensor Placement in Livestock Building

**Optimal locations (based on ventilation pattern analysis):**
1. **Exhaust duct:** Centralized measurement, representative of whole barn
   - Advantage: Mixed air, stable temperature
   - Challenge: High humidity, dust, cleaning access

2. **Animal breathing zone:** Direct exposure assessment
   - Height: 0.5-1.5m above floor
   - Spacing: One sensor per 20m² floor area
   - Challenge: Spatial variability, animal interference

**Selected for this demo: Exhaust duct mounting**

### Installation Requirements

**Mechanical:**
- Vibration damping: silicone shock mounts
- Access for maintenance: removable section of duct
- Sample inlet: 6mm OD stainless steel tube, 90° downward facing (dust protection)

**Electrical:**
- Power cable: shielded 2×1.5mm² for 12V DC
- Data cable: Belden 3105A twisted pair for RS-485
- Cable routing: separate conduits for power and signal (EMI reduction)
- Grounding: single-point ground at power supply (avoid ground loops)

**Data management:**
- Local storage: 32 GB = 2 years of data (1 sample/5 sec, 100 bytes/sample)
- Remote transmission: MQTT to central server every 5 minutes (60 samples batched)
- Redundancy: both local SD and remote storage (no data loss if network fails)

## Compliance and Standards

**Relevant standards reviewed:**
- ISO 16000-1: Indoor air quality sampling strategy
- EN 50081: EMC generic emission standard for industrial environments
- EN 50082: EMC generic immunity standard
- IEC 61000-4-2: ESD immunity
- IEC 60529: IP enclosure ratings

**Safety considerations:**
- ATEX certification **not required** (sensors are < 1W, incapable of ignition)
- Low voltage directive: 12V DC is Safety Extra-Low Voltage (SELV)
- RoHS compliance: all components selected from RoHS-compliant vendors

## Future Enhancements (Post-Demo)

1. **Multi-gas expansion:**
   - Add Alphasense IRC-A1 (CH₄) + N2O-A1 via Modbus
   - Estimated cost: +€180 per node

2. **LoRaWAN option:**
   - Replace WiFi with RFM95W module (868 MHz EU)
   - Benefit: 10 km range, very low power
   - Trade-off: Lower data rate, requires gateway

3. **Solar power:**
   - 10W panel + 12V 7Ah lead-acid battery
   - Autonomy: 7 days without sun
   - Cost: +€50 per node

4. **Advanced QA/QC:**
   - Sensor redundancy (2× NH₃ sensors with discrepancy alert)
   - Automatic baseline correction using diurnal minimums
   - Machine learning anomaly detection

## References

1. Alphasense Ltd. (2023). NH3-B1 Ammonia Sensor Datasheet.
2. Sensirion AG. (2023). SCD4x CO₂ Sensor Datasheet.
3. Espressif Systems. (2023). ESP32-WROOM-32E Datasheet.
4. Groot Koerkamp, P. W. G., et al. (1998). "Concentrations and emissions of ammonia in livestock buildings in Northern Europe." Journal of Agricultural Engineering Research, 70(1), 79-95.
5. Scholtens, R., et al. (2003). "Measures to reduce ammonia emissions from dairy cow houses." International Congress Series, 1293, 123-130.
6. VERA Protocol. (2018). "Verification of Environmental Technologies for Agricultural Production."
7. Modbus Organization. (2012). "Modbus Application Protocol Specification V1.1b3."
8. ISO 16000-1:2004. "Indoor air - Part 1: General aspects of sampling strategy."

---

**Document version:** 1.0  
**Date:** September 10, 2026  
**Author:** R. Abdollahipour  
**Purpose:** Hardware justification for MARVELA/ATB job application portfolio

# Professional Circuit Design and Integration

## Complete System Schematic

This document presents the production-ready circuit design for agricultural emission monitoring system with NH₃ electrochemical sensor, CO₂/RH/T I²C sensor, RS-485 Modbus interface, and local SD card logging.

## Block Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LIVESTOCK BUILDING MONITORING NODE                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐         ┌────────────────────────────────┐       │
│  │  12V DC      │         │     Input Protection            │       │
│  │  Power       ├────────►│  - TVS Diode (surge)           │       │
│  │  Supply      │         │  - Polyfuse (over-current)     │       │
│  └──────────────┘         │  - Reverse polarity MOSFET     │       │
│                            └───────┬────────────────────────┘       │
│                                    │                                 │
│                            ┌───────▼────────────────────────┐       │
│                            │  RECOM R-78E3.3-1.0            │       │
│                            │  Switching Regulator            │       │
│                            │  12V → 3.3V @ 1A                │       │
│                            └───────┬────────────────────────┘       │
│                                    │ 3.3V                            │
│         ┌──────────────────────────┼─────────────────────────────┐  │
│         │                          │                             │  │
│  ┌──────▼──────┐          ┌───────▼────────┐         ┌─────────▼──┐│
│  │  NH₃-B1     │          │   SCD41        │         │  microSD   ││
│  │ Electrochem │◄─────────┤  I²C Sensor    │         │   Card     ││
│  │  + TIA      │  I²C     │  (CO₂/RH/T)    │         │  (SPI)     ││
│  │  + ADC      │          └───────┬────────┘         └─────┬──────┘│
│  └──────┬──────┘                  │                        │        │
│         │                          │                        │        │
│         │ Analog    ┌──────────────▼────────────────────────▼──────┐│
│         └──────────►│         ESP32-WROOM-32E               │       ││
│                     │                                        │       ││
│                     │  • Dual-core processor                │       ││
│                     │  • WiFi + BLE                         │       ││
│                     │  • 12-bit ADC                         │       ││
│                     │  • 3× UART, 2× I²C, 4× SPI           │       ││
│                     └──────────────┬─────────────────────────┘      │
│                                    │                                 │
│                            ┌───────▼────────────────────────┐       │
│                            │     MAX3485                     │       │
│                            │   RS-485 Transceiver            │       │
│                            └───────┬────────────────────────┘       │
│                                    │                                 │
│                                    ▼                                 │
│                           A/B Twisted Pair                          │
│                       (to reference analyzer)                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Circuit Schematics

### 1. Power Supply and Protection Circuit

```
Input (J1)
    │
    │  P6KE15A              D1
12V ├──┤◄─────┐            1N5819
    │         │   F1          │
    ├─────────┴──[PF]─────────┤
    │         TVS   1A         │
    │                          │
    │        Q1 Si2301DS       │
    │         ┌──┐             │
    │      D  │  │ S           │
    └─────────┤  ├─────────────┤
         G    │  │             │
         │    └──┘             │
         │     P-MOSFET        │
        GND   (Reverse         │
             Protection)       │
                               │
    ┌──────────────────────────┘
    │
    │  C1
    ├───┤├───┐  1000µF
    │         │  35V
    │        GND
    │
    │  U1: RECOM R-78E3.3-1.0
    │         ┌───────┐
    │    VIN  │       │  VOUT    3.3V
    ├─────────┤   1   ├──────────┬──────
    │         │   2   │          │
    │    GND  │   3   │          │  C2
   GND ───────┤       ├───       ├──┤├──┐
              └───────┘  GND     │      │
                                 │     GND
                                 │
                        100µF    │
                        Ceramic  │
                                 │
                      To all ICs └──────► VCC (3.3V)
```

**Component specifications:**

| Designator | Part Number | Specs | Purpose |
|------------|-------------|-------|---------|
| D1 | P6KE15A | TVS, 600W, 15V | Surge protection |
| F1 | RXEF010 | Polyfuse, 1A hold | Over-current protection |
| Q1 | Si2301DS | P-MOSFET, -20V, -2.3A | Reverse polarity protection |
| D2 | 1N5819 | Schottky, 1A, 40V | Body diode |
| U1 | R-78E3.3-1.0 | Switching reg, 1A | Main 3.3V rail |
| C1 | EEU-FR1V102 | 1000µF, 35V, low-ESR | Input filtering |
| C2 | GRM31CR71C107KA01L | 100µF, 16V, X7R | Output filtering |

### 2. NH₃ Sensor and Signal Conditioning

```
        3.3V
         │
         │ R1
         ├─/\/\/\───┐  4.7kΩ (Pull-up for NTC)
         │          │
         │          │  R_NTC
         │          ├─/\/\/\──┐
         │          │         │
         │          │        GND
         │          │
         │          │  To ESP32 ADC_NTC (GPIO35)
         │          └───────────────────────►
         │
         │
    NH₃-B1 Sensor
    ┌────────┐
    │   WE   ├──────┐  Working Electrode
    │        │      │
    │   RE   ├──────┤  Reference Electrode (connected to WE)
    │        │      │
    │   AE   ├──────┤  Auxiliary Electrode
    └────────┘      │
                    │
         Current    │
         Output     │
      (50-90nA/ppm) │
                    │
    ┌───────────────▼──────────────┐
    │   Transimpedance Amplifier   │
    │                               │
    │           R_FEEDBACK          │
    │            33kΩ               │
    │    ┌──────/\/\/\─────┐       │
    │    │                 │       │
    │    │    U2: OPA2333  │       │
    │    │      ┌──────┐   │       │
    │    └──────┤-  OUT├───┴───────┼─────► V_NH3
    │           │      │           │
    │      ┌────┤+     │           │
    │      │    │      │           │
    │     VCC/2 └──────┘           │
    │    (1.65V)                   │
    │    R2, R3                    │
    │    10kΩ divider              │
    └──────────────────────────────┘
         │
         │  C3
         ├──┤├───┐  100nF (Anti-aliasing filter)
         │        │
         │       GND
         │
         └───────────────────► To ESP32 ADC (GPIO34)
                                 0-3.3V range
                                 12-bit (0-4095)
                                 
Signal Chain Analysis:
━━━━━━━━━━━━━━━━━━━━━
• NH₃ concentration: 0-50 ppm (normal operation)
• Sensor output: 50-90 nA/ppm (typical 70 nA/ppm)
• At 50 ppm: 50 × 70 = 3500 nA = 3.5 µA
• TIA output: 3.5 µA × 33kΩ = 115 mV above bias
• Bias voltage: 1.65V (mid-rail)
• Total output: 1.65V + 0.115V = 1.765V
• ADC reading: 1.765V / 3.3V × 4095 = 2190 counts
• Resolution: 1 ppm = 70nA × 33kΩ = 2.3mV = 2.9 ADC counts
```

**Component specifications:**

| Designator | Part Number | Specs | Purpose |
|------------|-------------|-------|---------|
| U2 | OPA2333 | Dual op-amp, chopper-stabilized | Low-noise TIA |
| R_FB | ERJ-6ENF3302V | 33kΩ, 1%, 25ppm/°C | TIA feedback |
| R1 | ERJ-6ENF4701V | 4.7kΩ, 1% | NTC pull-up |
| R2, R3 | ERJ-6ENF1002V | 10kΩ, 1% | Bias divider |
| C3 | GRM188R71H104KA93D | 100nF, 50V, X7R | Anti-aliasing |
| R_NTC | NTCG163JF103FT1 | 10kΩ @ 25°C, β=3380 | Temperature sense |

**Calibration equation:**

```python
# Raw ADC to voltage
V_adc = (adc_counts / 4095.0) * 3.3  # Volts

# Voltage to sensor current (removing bias)
V_bias = 1.65  # Volts
V_signal = V_adc - V_bias
I_sensor = V_signal / 33000  # Amperes

# Current to NH₃ concentration (from calibration)
# Typical sensitivity: 70 nA/ppm
# After lab calibration: slope and offset
sensitivity = 70e-9  # A/ppm (from datasheet, refined in lab)
NH3_ppm = I_sensor / sensitivity

# Temperature compensation (from NTC)
T_ref = 25  # °C
T_coeff = -0.5  # ppm/°C (from characterization)
NH3_compensated = NH3_ppm - (T_actual - T_ref) * T_coeff
```

### 3. I²C Sensor Interface (SCD41)

```
         3.3V
          │
          │  R4        R5
          ├─/\/\/\─┬─/\/\/\──┐
          │ 4.7kΩ  │  4.7kΩ  │
          │        │         │
          │        │         │
   ESP32  │        │         │    SCD41 Module
 ┌────────┴────────┴─────────┴──────────┐
 │                                       │
 │  GPIO21 (SDA) ───────────────► SDA   │
 │                                       │
 │  GPIO22 (SCL) ───────────────► SCL   │
 │                                       │
 │  3.3V ────────────────────────► VDD  │
 │                                       │
 │  GND ─────────────────────────► GND  │
 │                                       │
 └───────────────────────────────────────┘

I²C Configuration:
━━━━━━━━━━━━━━━━━
• Address: 0x62 (fixed, 7-bit)
• Clock: 100 kHz (standard mode)
• Pull-ups: 4.7kΩ (calculated for Cb ~100pF)
• Commands:
  - Start periodic measurement: 0x21B1
  - Read measurement: 0xEC05
  - Get serial number: 0x3682
• Data format: 16-bit words with 8-bit CRC
• Update interval: 5 seconds
```

**SCD41 Register Map:**

| Command | Code | Data Bytes | Response | Description |
|---------|------|------------|----------|-------------|
| start_periodic_measurement | 0x21B1 | 0 | None | Start 5-sec updates |
| read_measurement | 0xEC05 | 0 | 9 bytes | CO₂, T, RH with CRC |
| stop_periodic_measurement | 0x3F86 | 0 | None | Stop measurements |
| get_serial_number | 0x3682 | 0 | 9 bytes | 48-bit serial + CRC |
| perform_self_test | 0x3639 | 10 sec | 3 bytes | Sensor self-test |

**Data parsing example:**

```python
# Read 9 bytes: [CO2_H, CO2_L, CRC, T_H, T_L, CRC, RH_H, RH_L, CRC]
data = i2c.read(address=0x62, nbytes=9)

# CO₂ (ppm)
co2_raw = (data[0] << 8) | data[1]
# CRC check: crc8(data[0:2]) == data[2]
co2_ppm = co2_raw  # Direct value

# Temperature (°C)
temp_raw = (data[3] << 8) | data[4]
temp_degC = -45 + 175 * (temp_raw / 65535.0)

# Humidity (%)
rh_raw = (data[6] << 8) | data[7]
rh_percent = 100 * (rh_raw / 65535.0)
```

### 4. RS-485 Modbus Interface

```
         3.3V
          │
          │  R6
          ├─/\/\/\───┐  10kΩ
          │          │
          │          │  C4
          │          ├──┤├───┐  100nF (Decoupling)
          │          │       │
          │          │      GND
          │          │
          │   ┌──────▼─────────────────────┐
          │   │  U3: MAX3485CSA+           │
          │   │  (SO-8 package)            │
          │   │                            │
   ESP32  │   │  Pin 1: RO  (Receiver Out) │   ┌─── ESP32 GPIO16 (UART2_RX)
  GPIO17 ─┼───┼─► Pin 4: DI  (Driver In)   │   │
  (TX)    │   │                            │   │
          │   │  Pin 2: RE  (Receive En, active-LOW)  │
  GPIO27 ─┼───┼─► Pin 3: DE  (Driver En, active-HIGH) │
   (DIR)  │   │        (tied together)     │   │
          │   │                            │   │
          │   │  Pin 8: VCC (3.3V) ───────┼───┘
          │   │  Pin 5: GND ──────────────┼──── GND
          │   │                            │
          │   │  Pin 6: A  (Non-inverting) │
          │   │  Pin 7: B  (Inverting)     │
          │   └──────┬────────┬────────────┘
          │          │        │
          │         [A]      [B]   RS-485 Bus
          │          │        │
          │          │        │   R7 (Termination, install only at bus ends)
          │          └─/\/\/\─┘   120Ω, 0.5W
          │                │
          │               GND (through 10kΩ failsafe bias at ONE location)
          │
          │
   Twisted Pair Cable (Belden 3105A or equiv.)
   │
   │  Max 500m in this application
   │  120Ω characteristic impedance
   │  24 AWG, shielded
   │
   └─────────► To Reference Analyzer Modbus Port


Bus Biasing (at ONE location only, typically master):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      3.3V
       │
       │ R_BIAS_A
       ├──/\/\/\──┐  560Ω (pulls A towards VCC)
       │          │
       │         [A]
       │
       │ R_BIAS_B
      ─┴─/\/\/\──┐  560Ω (pulls B towards GND)
      GND         │
                 [B]

Purpose: Ensures defined idle state when no drivers active
```

**Component specifications:**

| Designator | Part Number | Specs | Purpose |
|------------|-------------|-------|---------|
| U3 | MAX3485CSA+ | 3.3V RS-485, 12Mbps | Differential transceiver |
| R6 | ERJ-6ENF1002V | 10kΩ, 1% | Pull-up for DE/RE |
| C4 | GRM188R71H104KA93D | 100nF, X7R | Power decoupling |
| R7 | CRCW0805120RFKEA | 120Ω, 1%, 0.5W | Bus termination |
| R_BIAS_A/B | ERJ-6ENF5600V | 560Ω, 1% | Idle bias (master side) |

**Modbus RTU Frame Example: Read 3 Registers from Address 0**

```
Request (from ESP32 to Reference Analyzer):
┌──────┬──────────┬──────────┬────────┬──────┬────────┐
│ Unit │ Function │  Start   │ Qty    │ CRC  │ CRC    │
│ ID   │   Code   │  Address │        │ Low  │ High   │
├──────┼──────────┼──────────┼────────┼──────┼────────┤
│ 0x01 │   0x03   │  0x0000  │ 0x0003 │ 0xXX │ 0xXX   │
└──────┴──────────┴──────────┴────────┴──────┴────────┘
   1       1          2          2        2 bytes
  byte    byte       bytes      bytes

Hex: 01 03 00 00 00 03 05 CB

Response (from Reference Analyzer):
┌──────┬──────────┬──────┬────────┬────────┬────────┬────────┐
│ Unit │ Function │ Byte │  NH₃   │  CH₄   │  N₂O   │  CRC   │
│ ID   │   Code   │ Count│ (word) │ (word) │ (word) │        │
├──────┼──────────┼──────┼────────┼────────┼────────┼────────┤
│ 0x01 │   0x03   │ 0x06 │ 0x04E2 │ 0x0320 │ 0x003C │ 0xXXXX │
└──────┴──────────┴──────┴────────┴────────┴────────┴────────┘
   1       1        1       2        2        2        2
  byte    byte    byte    bytes    bytes    bytes    bytes

Hex: 01 03 06 04 E2 03 20 00 3C XX XX

Decoding:
• NH₃: 0x04E2 = 1250 → 1250/100 = 12.50 ppm
• CH₄: 0x0320 = 800 → 800/100 = 8.00 ppm
• N₂O: 0x003C = 60 → 60/1000 = 0.060 ppm
```

**UART Configuration for Modbus RTU:**

```c
// ESP32 UART2 initialization
uart_config_t uart_config = {
    .baud_rate = 9600,              // Standard for field instruments
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_EVEN,     // 8E1 is Modbus standard
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    .source_clk = UART_SCLK_APB,
};

// Frame timing (critical for Modbus RTU)
// Character time: 11 bits / 9600 bps = 1.146 ms
// Inter-character timeout: 1.5 × 1.146 ms = 1.7 ms
// Frame gap: 3.5 × 1.146 ms = 4.0 ms
```

### 5. microSD Card Interface (SPI)

```
         3.3V
          │
          │  R8
          ├─/\/\/\───┐  10kΩ (CS pull-up)
          │          │
   ESP32  │          │     microSD Card Module
 ┌────────┴──────────┴────────────────────┐
 │                                         │
 │  GPIO23 (MOSI) ──────────────► DI      │
 │                                         │
 │  GPIO19 (MISO) ◄─────────────── DO     │
 │                                         │
 │  GPIO18 (SCK)  ──────────────► CLK     │
 │                                         │
 │  GPIO5  (CS)   ──────────────► CS      │
 │                                         │
 │  3.3V ────────────────────────► VCC    │
 │                                         │
 │  GND ─────────────────────────► GND    │
 │                                         │
 └─────────────────────────────────────────┘

SD Card Selection:
━━━━━━━━━━━━━━━━━
• Type: microSDHC (High Capacity)
• Size: 32 GB
• Class: UHS-I U3 (min 30 MB/s sustained write)
• Endurance: High Endurance or Industrial grade
• Format: FAT32
• Example: SanDisk High Endurance SDSQQNR-032G

File Structure:
/
├── config.json       (system configuration)
├── calibration.json  (sensor coefficients)
├── logs/
│   ├── 2026-09-10.csv
│   ├── 2026-09-11.csv
│   └── ...

CSV Format:
timestamp,sequence,nh3_ppm,nh3_raw_mV,co2_ppm,temp_c,rh_percent,quality_flags,modbus_nh3,modbus_ch4,modbus_n2o,network_status
2026-09-10T14:30:00Z,12345,12.5,1765,850,22.3,65.2,0x00,12.50,8.00,0.060,ONLINE
```

**SPI Configuration:**

```c
// ESP32 SPI initialization for SD card
spi_bus_config_t bus_cfg = {
    .mosi_io_num = 23,
    .miso_io_num = 19,
    .sclk_io_num = 18,
    .quadwp_io_num = -1,    // Not used
    .quadhd_io_num = -1,    // Not used
    .max_transfer_sz = 4000,
};

// SD card specific settings
sdmmc_host_t host = SDSPI_HOST_DEFAULT();
host.max_freq_khz = SDMMC_FREQ_DEFAULT;  // 20 MHz

// Important: GPIO5 has pull-up at boot (strapping pin)
// Verify SD card doesn't interfere with boot mode
```

### 6. Complete Pin Assignment Summary

| GPIO | Direction | Function | Connected To | Notes |
|------|-----------|----------|--------------|-------|
| 4 | Digital In | DHT22 (demo) | DHT22 DATA | 10kΩ pull-up, demo only |
| 5 | Digital Out | SPI CS | SD Card CS | Strapping pin, check boot |
| 16 | Digital In | UART2 RX | MAX3485 RO | Modbus receive |
| 17 | Digital Out | UART2 TX | MAX3485 DI | Modbus transmit |
| 18 | Digital Out | SPI CLK | SD Card CLK | Hardware SPI |
| 19 | Digital In | SPI MISO | SD Card DO | Hardware SPI |
| 21 | Bidirectional | I²C SDA | SCD41 SDA | 4.7kΩ pull-up |
| 22 | Digital Out | I²C SCL | SCD41 SCL | 4.7kΩ pull-up |
| 23 | Digital Out | SPI MOSI | SD Card DI | Hardware SPI |
| 27 | Digital Out | RS-485 DIR | MAX3485 DE/RE | Direction control |
| 34 | Analog In | ADC1_CH6 | NH₃ TIA output | 0-3.3V, 12-bit |
| 35 | Analog In | ADC1_CH7 | NTC thermistor | Temperature comp |
| 2 | Digital Out | LED | Status LED | Acquisition indicator |

**Unused but reserved for future expansion:**
- GPIO12, 13, 14, 15: Additional SPI or GPIO
- GPIO25, 26: DAC outputs for analog control
- GPIO32, 33: Additional ADC inputs

## PCB Layout Considerations

### 2-Layer PCB Stackup

```
┌─────────────────────────────────────┐
│  TOP LAYER (Signal + Power)         │
│  • Components                        │
│  • 3.3V power plane (polygon)       │
│  • Signal traces                    │
├─────────────────────────────────────┤
│  BOTTOM LAYER (Ground + Power)      │
│  • Ground plane (continuous)        │
│  • Return paths                     │
│  • 12V input traces                 │
└─────────────────────────────────────┘

Dimensions: 100 × 80 mm
Thickness: 1.6 mm
Copper: 1 oz (35 µm) both layers
Finish: ENIG (Electroless Nickel Immersion Gold)
Solder mask: Green (LPI)
Silkscreen: White (both sides)
```

### Critical Layout Rules

**1. Power distribution:**
- 12V input trace: 1.0 mm width (for 271 mA, very conservative)
- 3.3V traces: 0.5 mm width
- Ground plane: Uninterrupted, maximum copper area
- Star grounding: All decoupling caps connect to single point per IC

**2. Analog section isolation:**
```
         DIGITAL SECTION              |       ANALOG SECTION
                                      |
   ┌──────────────┐                  |   ┌──────────────┐
   │   ESP32      │                  |   │  NH₃ Sensor  │
   │   (Digital)  │    Ferrite Bead  |   │  + TIA       │
   │              ├───────────/\/────┼───┤  (Analog)    │
   │   3.3V       │     FB1          |   │  3.3V_A      │
   └──────────────┘                  |   └──────────────┘
         │                            |         │
        GND                           |       GND_A
         │                            |         │
         └────────────────────────────┴─────────┘
                  SINGLE POINT GROUND
                  (near power supply)
```

**3. High-speed signals:**
- SPI traces (CLK, MOSI, MISO): 0.3 mm width, keep < 50 mm length
- I²C traces: 0.3 mm width, matched length ±5 mm
- RS-485 differential pair:
  - Trace width: 0.25 mm
  - Spacing: 0.25 mm (100Ω differential impedance)
  - Length matching: ±1 mm
  - Keep away from switching regulator by 5 mm minimum

**4. Component placement:**
```
          TOP VIEW
┌──────────────────────────────────┐
│  J1                           J2 │  J1: 12V input
│  Power   ┌─────────┐   RS-485    │  J2: RS-485 A/B
│  Input   │  U1     │   Output    │  J3: I²C sensor
│          │ Regul.  │             │  J4: SD card slot
│          └─────────┘             │
│                                  │
│   ┌────────────┐      ┌───┐     │
│   │            │      │U3 │ J3  │
│   │   ESP32    │      │485│ Sensor
│   │  WROOM-32E │      └───┘     │
│   │            │                │
│   └────────────┘   ┌──────┐    │
│                    │ U2   │    │
│      J4            │ TIA  │    │
│   ┌──────┐         └──────┘    │
│   │ SD   │    Analog Section   │
│   │ Card │    (keep isolated)  │
│   └──────┘                     │
└──────────────────────────────────┘
```

### Design for Manufacturing (DFM) Guidelines

**Minimum specifications:**
- Trace width: 0.15 mm (signal), 0.5 mm (power)
- Trace spacing: 0.15 mm
- Via diameter: 0.4 mm drill, 0.8 mm pad
- Annular ring: 0.2 mm minimum
- Solder mask expansion: 0.1 mm
- Silkscreen width: 0.15 mm (6 mil)
- Silkscreen clearance: 0.15 mm from pads

**Panelization:** 5 boards per panel (100×400 mm), V-score separation

## Testing and Commissioning Procedure

### Step 1: Visual Inspection (Unpowered)

- [ ] Inspect solder joints under magnification (10×)
- [ ] Check for solder bridges, cold joints, tombstoning
- [ ] Verify component orientation (ICs, electrolytic caps, LEDs)
- [ ] Check mechanical fit of connectors

### Step 2: Electrical Checks (Unpowered)

- [ ] Measure resistance between VCC and GND: expect > 1 kΩ
- [ ] Check continuity of ground plane
- [ ] Verify no shorts between power rails
- [ ] Test reverse polarity protection: apply -12V, no connection to circuit

### Step 3: Power-Up Sequence

**3.1 Initial power application:**
1. Set bench supply to 12.0V, current limit 0.5A
2. Connect via current meter
3. Observe inrush current: expect < 200 mA
4. Steady-state: expect 100-150 mA (no WiFi active)

**3.2 Voltage rail verification:**
- [ ] Measure 3.3V rail: expect 3.25-3.35V
- [ ] Measure under 500 mA load: dropout < 50 mV
- [ ] Check ripple with oscilloscope: < 100 mV p-p

### Step 4: Subsystem Testing

**4.1 Microcontroller:**
- [ ] ESP32 boots (LED flashes)
- [ ] Serial console responds (115200 baud)
- [ ] WiFi MAC address readable
- [ ] Flash memory test passes

**4.2 I²C sensor:**
```python
import smbus2
bus = smbus2.SMBus(1)
# Read SCD41 serial number
bus.write_i2c_block_data(0x62, 0x36, [0x82])
time.sleep(0.01)
serial = bus.read_i2c_block_data(0x62, 0, 9)
print(f"SCD41 Serial: {serial.hex()}")
# Expected: 9 bytes with valid CRC
```

**4.3 SD card:**
```c
// Test write speed
File file = SD.open("/test.bin", FILE_WRITE);
uint32_t start = millis();
for(int i=0; i<1000; i++) {
    file.write(buffer, 512);  // 512 bytes
}
file.close();
uint32_t elapsed = millis() - start;
float speed_kBps = (1000 * 512) / elapsed;
// Expected: > 500 kB/s for Class 10 card
```

**4.4 RS-485:**
- [ ] Measure idle differential voltage: |VA - VB| = 200-400 mV
- [ ] Transmit test pattern, capture on oscilloscope
- [ ] Verify rise/fall times < 100 ns
- [ ] Check eye diagram for jitter

**4.5 Analog (NH₃ sensor):**
```python
# Inject known current
I_test = 1.0e-6  # 1 µA
R_feedback = 33000  # Ω
V_expected = 1.65 + I_test * R_feedback  # = 1.683V

adc_raw = esp32.read_adc(GPIO34)
adc_voltage = (adc_raw / 4095.0) * 3.3
error_mV = abs(adc_voltage - V_expected) * 1000

print(f"Expected: {V_expected:.3f}V")
print(f"Measured: {adc_voltage:.3f}V")
print(f"Error: {error_mV:.1f} mV")
# Acceptable: < 10 mV
```

### Step 5: Integrated System Test

**5.1 Continuous operation test:**
- Run for 24 hours at 25°C
- Log all measurements to SD card
- Verify no resets, no data loss
- Check file integrity

**5.2 Temperature cycling:**
- -10°C → 40°C → -10°C (3 cycles)
- Monitor voltage rails (< 5% variation)
- Verify sensor readings remain valid

**5.3 Power interruption:**
- Remove power for 10 seconds
- Restore power
- Verify clean reboot, SD card accessible
- Check last timestamp (should show gap, not corruption)

**5.4 Communication stress test:**
- Modbus: 1000 read cycles, check error rate < 0.1%
- WiFi: 1000 MQTT publishes, check delivery > 99%
- SD: Write 1 GB data, verify integrity with checksum

## Production Documentation

### Files to Generate

1. **Schematic (PDF)** - KiCad or Altium source
2. **PCB layout (PDF)** - All layers separately
3. **Bill of Materials (Excel)** - With vendor part numbers
4. **Assembly drawing (PDF)** - Component placement, orientation
5. **Gerber files (ZIP)** - RS-274X format for manufacturer
6. **Pick-and-place (CSV)** - Centroid coordinates for PCBA
7. **Test procedure (PDF)** - This section as checklist
8. **Calibration certificate template** - For each unit

### Manufacturing Partner Selection

**Recommended vendors (as of 2026):**
- **PCB fabrication:** JLCPCB, PCBWay, Eurocircuits
- **Assembly:** JLCPCB PCBA, Macrofab, Screaming Circuits
- **Enclosure:** Hammond direct or distributor
- **Components:** Mouser Electronics, Digi-Key, Farnell

**Lead times:**
- PCB bare boards: 5-10 days
- Full assembly: 15-20 days
- Sensors (Alphasense): 4-6 weeks (long lead item!)
- Total project time: Plan 8-10 weeks for first batch

---

**Document version:** 1.0  
**Date:** September 10, 2026  
**Author:** R. Abdollahipour  
**Purpose:** Circuit design documentation for MARVELA/ATB application

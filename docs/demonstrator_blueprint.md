# Bench-to-Barn Engineering Demonstrator — Master Blueprint

This document defines the **redesigned project narrative** for the MARVELA/ATB microcontroller role and David Janke’s emphasis on **hands-on, demonstrative engineering**. It replaces “simulator-only portfolio” with a **hybrid demonstrator** that is honest about what is simulated, bench-tested, or design-stage.

## One-sentence pitch

> A modular IoT livestock monitoring node—designed for an **LVAT-like experimental farm**, demonstrated from **sensor selection** through **pin-exact simulation**, **PCB/assembly**, **driver commissioning**, **QA/QC**, and **barn-scale data flow**.

## Design principles

1. **No fabricated evidence** — photos, voltages, and campaign results only after real work (`physical_prototype/`).
2. **Wokwi is a layer, not the whole story** — use it for pin-level integration and firmware demo; use bench + KiCad for hands-on and deployable design.
3. **Two sensor tracks** — Wokwi-supported parts for simulation; agricultural targets (NH₃-B1, SCD41) for design and bench where hardware exists.
4. **Every job-ad keyword maps to a visible artifact** — see [requirement_matrix.md](requirement_matrix.md).

---

## Seven-layer demonstrator stack

| Layer | Purpose | Primary artifacts |
|-------|---------|-------------------|
| 1. Farm context | Why and where the node lives | [farm_context.md](farm_context.md) |
| 2. Sensor selection & procurement | Choosing parts from scratch | [sensor_procurement.md](sensor_procurement.md), [hardware_selection.md](hardware_selection.md) |
| 3. Exact embedded simulation | Pin-to-pin integration + firmware | `wokwi/diagram.json`, PlatformIO, Wokwi VS Code |
| 4. PCB / assembly | Deployable hardware + manual solder points | `hardware/kicad/` (planned), `physical_prototype/photos/` |
| 5. Driver install & configuration | Firmware libs + host USB-UART | [driver_configuration.md](driver_configuration.md), [hardware_commissioning.md](hardware_commissioning.md) |
| 6. Commissioning & troubleshooting | Measured pass/fail, fault logs | [bench_commissioning_report.md](bench_commissioning_report.md) |
| 7. Barn data ecosystem | End-to-end flow, QA, dashboard | [ecosystem_overview.md](ecosystem_overview.md), Streamlit dashboard |

---

## Simulation strategy: Wokwi yes, but hybrid

### What Wokwi is good for ([Wokwi docs](https://docs.wokwi.com/guides/esp32))

- ESP32 + **DHT22**, **DS18B20**, **BMP180**, **MQ-2**, microSD, LEDs, resistors
- Exact **GPIO wiring** visible in `diagram.json`
- Firmware compile/run via **Wokwi for VS Code** + prebuilt `.bin` (`wokwi/flasher_args.json`)
- Serial monitor, basic fault injection (disconnect sensor wire in diagram)

### What Wokwi cannot honestly claim

- Two **humidity** sensor models for side-by-side comparison (catalog: essentially **DHT22 only**)
- Valid NH₃ electrochemical front-end
- Physical soldering, RS-485 bus electrical behaviour, OS driver install
- LVAT barn layout from website alone

### Decision: Option 2 (recommended)

| Quantity | Wokwi simulation | Real bench |
|----------|------------------|------------|
| Temperature | **DHT22** vs **DS18B20** (redundant T) | Optional third reference (PT100 / IR) |
| Humidity | **DHT22** (single official humidity part) | **SCD41** vs DHT22 comparison |
| Pressure | **BMP180** on I²C | — |
| Gas (surrogate) | **MQ-2** analog on GPIO34 | Design-stage NH₃-B1 only |
| CO₂ | — | **SCD41** (`esp32dev_scd41`) |

**Interview line:** *“Wokwi proves integration and firmware paths with catalog-supported sensors; humidity benchmarking and CO₂ use a real I²C module on the bench.”*

---

## Target node — pin map (hero simulation)

Aligned with `firmware/include/Config.h` (extensions in Phase 2):

| Signal | GPIO | Interface | Wokwi part |
|--------|------|-----------|------------|
| DHT22 DATA | 4 | Digital + 10 kΩ pull-up | `wokwi-dht22` |
| DS18B20 DATA | 15 | 1-Wire + 4.7 kΩ pull-up | `wokwi-ds18b20` |
| BMP180 SDA/SCL | 21 / 22 | I²C | `wokwi-bmp180` |
| MQ-2 AO | 34 | ADC1 (simulator only) | `wokwi-gas-sensor` |
| microSD | 5,18,19,23 | SPI | `wokwi-microsd-card` |
| RS-485 UART | 17 TX, 16 RX, 27 DE/RE | UART2 | `wokwi-ssd1306` N/A — use custom or MAX485 part if available; else bench-only |
| Status LED | 2 | GPIO | `wokwi-led` |

RS-485: Wokwi may not expose a standard MAX485 part in all projects—show **UART + DE pin** in diagram where possible; full transceiver on **perfboard/PCB photos**.

---

## PCB: required or not?

| Level | Needed for demo? | Shows |
|-------|------------------|-------|
| Breadboard / perfboard | **Yes** — minimum for David | Wiring, soldering, troubleshooting |
| KiCad 2-layer carrier | **Recommended** — engineering completeness | Terminals, protection, production path |
| Fabricated PCB assembly | Optional before interview | Manufacturability |

**Manual solder points to document** (photos + checklist):

- ESP32 header pins
- Screw terminals (12 V in, RS-485 A/B)
- DS18B20 pull-up resistor
- LED + 220 Ω
- microSD module header
- Optional MAX485 module pads

---

## “Installing and configuring drivers” — two meanings

Both must appear in the demonstrator:

### A. Firmware / peripheral drivers

Libraries and init for DHT, OneWire, Wire/I²C, SD/SPI, UART, Modbus, MQTT — see [driver_configuration.md](driver_configuration.md).

### B. Host / development drivers

CP210x/CH340 USB-UART, COM port, PlatformIO env, flash, serial monitor — see [hardware_commissioning.md](hardware_commissioning.md).

---

## Data path (summary)

See [ecosystem_overview.md](ecosystem_overview.md) for the full graphic.

```text
LVAT-like barn → sensor node → local SD + QA flags
              → RS-485 (reference Modbus) [bench]
              → WiFi/MQTT → broker → dashboard / CSV / SQLite
```

---

## What we do **not** claim (until evidence exists)

- Physical installation at LVAT Gross Kreutz
- NH₃ calibration against reference analyzer
- Farm campaign dataset
- Production-ready PCB in the field

---

## Related documents

- [implementation_roadmap.md](implementation_roadmap.md) — phased repo work
- [requirement_matrix.md](requirement_matrix.md) — job ad keyword → artifact
- [farm_context.md](farm_context.md) — deployment scenario
- [limitations.md](limitations.md) — transparency

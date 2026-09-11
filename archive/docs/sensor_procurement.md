# Sensor Procurement Workflow

This document supports **selecting and procuring sensors from scratch**—the process described in the MARVELA/ATB microcontroller role. It is a decision framework, not a claim that all listed parts have been purchased or installed.

## Process

1. Define measurement requirement (gas, range, environment, interface, maintenance).
2. Shortlist candidates from datasheets and agricultural literature.
3. Score against criteria; document **rejected** alternatives with reason.
4. Check EU availability, lead time, and calibration burden.
5. Order; record part number, vendor, date, and received serial/lot if applicable.
6. Store datasheet link in BOM; add bench evidence under `physical_prototype/` after integration.

---

## NH₃ (livestock barn, research-grade target)

| Criterion | Requirement | Alphasense NH₃-B1 | Notes |
|-----------|-------------|-------------------|-------|
| Measurand | NH₃ in air | Electrochemical | Biased three-electrode |
| Typical barn range | 0–50 ppm | 0–100 ppm spec range | Validate vs application |
| Sensitivity | Stable over months | 20–60 nA/ppm (datasheet) | Requires potentiostat / TIA |
| Interface | Analog + conditioning | Current output | Not direct GPIO |
| Cross-sensitivity | Documented | H₂S, NO₂, etc. in datasheet | Lab evaluation needed |
| Humidity | High RH in barns | Specified operating RH | Condensation risk at inlet |
| EU availability | Required for ATB work | Distributors in EU | Check lead time |
| Calibration | Acceptable for lab | Zero + span, periodic replacement | Filter and inlet design |

**Current decision:** NH₃-B1 documented as **design target**; no physical NH₃ channel commissioned in this repository yet.

**Rejected for this prototype stage (examples):**

| Candidate | Reason not selected now |
|-----------|-------------------------|
| MQ-2 / generic MOS | Not NH₃-selective; simulator surrogate only |
| Low-cost analog “NH₃ modules” | Unclear metrology traceability |
| TDLAS / FTIR inline | Cost and complexity beyond bench scope |

---

## CO₂ / RH / T (bench-realistic I²C module)

| Criterion | Requirement | Sensirion SCD41 | Notes |
|-----------|-------------|-----------------|-------|
| CO₂ range | 400–5000 ppm barn | 400–5000 ppm | Suitable for ventilation studies |
| RH / T | Co-located with CO₂ | On-chip | Single I²C module |
| Interface | I²C | 0x62 | Driver in `firmware/src/Scd41.cpp` |
| Power | 3.3 V | 3.3–5.5 V | Bench on 3.3 V |
| ASC / drift | Understand for long runs | ASC enabled in module | Document in validation plan |

**Current decision:** SCD41 selected for **bench I²C integration**; firmware driver available via `esp32dev_scd41` environment.

---

## RS-485 transceiver (reference analyzer / Modbus bench)

| Criterion | Requirement | MAX3485 / MAX485 class | Notes |
|-----------|-------------|------------------------|-------|
| Bus | Modbus RTU | Half-duplex RS-485 | Matches firmware `Rs485Transport` |
| Logic level | 3.3 V UART | 3.3 V compatible module | DE/RE tied to GPIO27 |
| Termination | 120 Ω at bus ends | External resistor | Only when topology requires |

**Current decision:** Protocol implemented and host-tested; **physical RS-485 assembly evidence pending** in `physical_prototype/`.

---

## Procurement log (fill when parts are ordered)

| Date | Part | Vendor | Order ref | Received | Bench test date |
|------|------|--------|-----------|----------|-----------------|
| TBD | ESP32-DevKitC | | | | |
| TBD | SCD41 breakout | | | | |
| TBD | MAX485 module | | | | |
| TBD | microSD + socket | | | | |

---

## References

- [hardware_selection.md](hardware_selection.md) — BOM and datasheet links
- [circuit_design.md](circuit_design.md) — interface design
- [bench_commissioning_report.md](bench_commissioning_report.md) — measured results after assembly

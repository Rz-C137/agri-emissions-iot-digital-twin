# Physical Bench Prototype

This directory holds **evidence from real hardware work** on the measurement node. Nothing here is generated or simulated.

## Purpose (aligned with hands-on commissioning)

The repository already documents virtual commissioning, firmware architecture, and design-stage schematics. This folder is where **measured** bench results, wiring photos, and troubleshooting logs belong after you assemble and test hardware in the lab.

## What belongs here

| Path | Content | Status |
|------|---------|--------|
| `photos/` | Real photos of ESP32 wiring, RS-485 module, soldering, bench setup | **Add after assembly** |
| `wiring/pin_assignment.md` | As-built pin map (may differ from design if bench uses DHT22 vs SCD41) | Template ready |
| `wiring/wiring_diagram.svg` | As-built wiring (export from lab notebook or draw.io) | **Add after assembly** |
| `commissioning/commissioning_checklist.md` | Pre-power and post-power checks | Template ready |
| `commissioning/voltage_measurements.csv` | Measured rail voltages | **Fill with real values** |
| `commissioning/rs485_test_results.csv` | Modbus loopback / adapter test log | **Fill after RS-485 test** |
| `commissioning/sensor_test_results.csv` | DHT22 / SCD41 / analog channel readings | **Fill after sensor test** |
| `troubleshooting/troubleshooting_log.md` | Dated problems, diagnosis, resolution | **Add as issues occur** |

## Minimum credible bench node (Phase 1)

```text
ESP32 devkit
  ├── DHT22 or SCD41 (environmental)
  ├── microSD (SPI)
  ├── optional MAX485 + USB–RS485 adapter (Modbus bench)
  └── status LED
```

NH₃/CH₄/N₂O remain **design-stage or virtual** until research-grade sensors and calibration facilities are available.

## Rules

1. **No fabricated photos or CSV rows.** If a test was not run, leave the file empty or mark `TBD`.
2. **Date every entry** in commissioning and troubleshooting logs.
3. **Link evidence** from `docs/07_commissioning.md` once measurements exist.

## Related documentation

- [Sensor selection and procurement](../docs/03_sensor_selection.md)
- [Commissioning workflow](../docs/07_commissioning.md)
- [Driver configuration](../docs/06_driver_configuration.md)
- [Physical bench plan](../docs/09_physical_bench_plan.md)
- [Limitations](../docs/12_limitations.md)

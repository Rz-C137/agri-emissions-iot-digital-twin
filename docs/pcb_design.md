# PCB Design — Carrier Board Concept

**Status:** Concept / Phase 3. The **breadboard prototype** is the minimum demonstrator for hands-on skills; this document describes the **production path** without claiming a fabricated PCB exists yet.

## Why include PCB in the demonstrator?

- Shows you can move from **quick prototype** to **deployable hardware**
- Supports David’s criteria: robust integration, terminals, field wiring
- Complements Wokwi pin-level simulation with **physical interconnect design**

## Block diagram (carrier)

```text
12 V in ──► protection ──► 3.3 V reg ──► ESP32 module socket
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    Sensor headers        microSD header      MAX485 + terminals
    (DHT, 1-Wire, I²C)   (SPI)               (A, B, GND)
```

## Connectors (planned)

| Connector | Function |
|-----------|----------|
| J1 | 12 V DC input (reverse protection) |
| J2 | ESP32 DevKit header (or WROOM socket) |
| J3 | Field sensor cable (DHT / 1-Wire / I²C) |
| J4 | RS-485 A, B, GND screw terminals |
| J5 | microSD module (SPI) |

## Manual soldering points (document with photos)

Listed in [demonstrator_blueprint.md](demonstrator_blueprint.md) — every through-hole joint on the first assembled carrier should appear in `physical_prototype/photos/`.

## KiCad project location

When started: [`hardware/kicad/`](../hardware/kicad/README.md)

## Related

- [circuit_design.md](circuit_design.md) — analog and power concepts
- [hardware.md](hardware.md) — pin assignment

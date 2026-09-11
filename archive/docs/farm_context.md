# Farm Context — LVAT-Like Livestock Building Demonstrator

## Site reference (honest framing)

The scenario is inspired by the **[Lehr- und Versuchsanstalt für Tierzucht und Tierhaltung (LVAT) e.V.](https://www.lvatgrosskreutz.de/)** — a teaching and experimental institution for livestock production near Potsdam, with educational content on emission-related topics in animal husbandry.

**We do not claim** to have extracted barn floor plans or installation permits from the public website. This repository defines an **LVAT-like experimental livestock building demonstrator** suitable for MARVELA/ATB discussion: modular nodes, lab validation, and future field trials.

## Monitoring objective (MARVELA alignment)

Continuous observation of:

- **Environmental parameters** — temperature, humidity, pressure (proxy for ventilation context)
- **Gas surrogates / future NH₃ channel** — low-cost sensing path vs reference instruments
- **System health** — storage, network, sensor faults

Target gases in the full project (design-stage here): NH₃, CH₄, N₂O, CO₂ — see [hardware_selection.md](hardware_selection.md).

## Installation concept

```text
                    ┌─────────────────────────────┐
                    │   Livestock building        │
                    │   (LVAT-like experimental)  │
                    │                             │
   Exhaust /       │   ┌─────┐                   │
   sampling zone ───┼──►│Node │  service access   │
                    │   └──┬──┘                   │
                    │      │ cable tray          │
                    └──────┼─────────────────────┘
                           │
                     Lab / edge PC
                     (commissioning, MQTT)
```

### Placement options (design discussion)

| Location | Pros | Cons |
|----------|------|------|
| Service alley, 2 m height | Maintenance access, less direct animal contact | May not match exhaust plume |
| Exhaust duct sampling port | Closer to emission stream | Heated, corrosive, needs inlet design |
| Indoor breathing zone | Representative animal environment | Dust, RH, NH₃ stress on electronics |

**Demonstrator choice:** service-area mount for **bench-to-barn narrative**; exhaust port documented as production option in [deployment_guide.md](deployment_guide.md).

## Environmental stressors (drive enclosure & QA)

- High **relative humidity** and condensation risk
- **Dust** and ammonia corrosion (long-term)
- **Temperature** roughly −10 °C to +35 °C (seasonal barn)
- **Vibration** and wash-down near some zones
- **Power** — 12 V field supply vs USB bench power

## Campaign workflow (future field stage)

1. Site survey and installation checklist  
2. Power and network verification  
3. Co-location with reference instrument (when available)  
4. 7–14 day logging campaign  
5. QA/QC, statistical comparison, uncertainty notes  

Templates: [bench_commissioning_report.md](bench_commissioning_report.md), [validation_protocol.md](validation_protocol.md).

## Link to demonstrator layers

| Farm need | Repo response |
|-----------|---------------|
| Why this node? | This document |
| Which sensors? | [sensor_procurement.md](sensor_procurement.md) |
| How wired? | `wokwi/diagram.json`, [hardware.md](hardware.md) |
| How commissioned? | `physical_prototype/`, [hardware_commissioning.md](hardware_commissioning.md) |
| How data flows? | [ecosystem_overview.md](ecosystem_overview.md) |

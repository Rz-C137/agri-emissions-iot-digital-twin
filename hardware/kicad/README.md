# KiCad PCB Design (Planned — Phase 3)

Carrier board for the ESP32 livestock monitoring node: screw terminals, sensor headers, RS-485 transceiver site, microSD module header, 12 V input protection, 3.3 V regulation.

**Status:** Not started. Breadboard evidence lives in [`physical_prototype/`](../physical_prototype/README.md) first.

## Planned contents

```text
hardware/kicad/
├── agri_node/
│   ├── agri_node.kicad_pro
│   ├── agri_node.kicad_sch
│   └── agri_node.kicad_pcb
├── bom/
│   └── carrier_bom.csv
└── exports/
    ├── schematic.pdf
    └── pcb_front.png
```

## Hand-solder vs machine assembly (documentation intent)

| Item | Assembly |
|------|----------|
| ESP32 module header | Hand solder |
| Screw terminals (power, RS-485 A/B) | Hand solder |
| Pull-up resistors, LED | Hand solder |
| Optional SMD passives on carrier | Reflow or hand |

See [implementation_roadmap.md](../docs/implementation_roadmap.md) Phase 3.

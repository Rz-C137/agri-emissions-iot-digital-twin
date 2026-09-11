# Implementation Roadmap — Redesign to Demonstrator

Phased plan to evolve the repo from **virtual twin** to **bench-to-barn engineering demonstrator**. Each phase adds **honest** evidence; no synthetic photos or measurements.

---

## Phase 0 — Narrative & mapping (current)

- [x] [demonstrator_blueprint.md](demonstrator_blueprint.md)
- [x] [farm_context.md](farm_context.md)
- [x] [ecosystem_overview.md](ecosystem_overview.md)
- [x] [requirement_matrix.md](requirement_matrix.md)
- [x] [driver_configuration.md](driver_configuration.md)
- [x] `physical_prototype/` templates
- [x] SCD41 firmware driver (`esp32dev_scd41`)

---

## Phase 1 — Hero Wokwi node (1–2 weeks)

**Goal:** Pin-exact multi-sensor diagram + firmware paths David can see in Wokwi VS Code.

| Task | Deliverable | Status |
|------|-------------|--------|
| Add DS18B20 to `diagram.json` | GPIO15 + pull-up | ✅ |
| Add BMP180 on I²C | GPIO21/22 | ✅ |
| Modular sensor drivers + `SensorManager` | `Dht22Sensor`, `Ds18b20Sensor`, `Bmp180Sensor`, `AnalogGasSensor` | ✅ |
| Temperature QA/QC | `QualityControl.cpp`, `# TEMP_QC` serial line, `TEMP_SENSOR_DISAGREEMENT` | ✅ |
| Update `tools/generate_figures.py` | Wiring validation | ✅ |
| Dashboard | **Sensor Commissioning** page with fault injection | ✅ |
| Wokwi VS Code | `pio run` + `prepare_wokwi_firmware.py` + open `diagram.json` | ✅ documented |
| Streamlit Wokwi embed | Deprioritized (cloud build unreliable) | — |

**Not in Phase 1:** NH₃ analog front-end in Wokwi.

---

## Phase 2 — Real bench minimum (1–2 weeks)

**Goal:** Hands-on evidence for David’s email.

| Task | Deliverable |
|------|-------------|
| Assemble ESP32 + DHT22 or SCD41 + SD on breadboard | Photos in `physical_prototype/photos/` |
| Optional MAX485 + USB adapter | `rs485_test_results.csv` filled |
| Measure 3.3 V rail | `voltage_measurements.csv` |
| Complete commissioning checklist | Signed checklist scan optional |
| Humidity compare | DHT22 vs SCD41 on bench (not Wokwi) |
| Troubleshooting log | At least one real entry (e.g. USB driver) |

---

## Phase 3 — PCB & assembly story (2–3 weeks)

**Goal:** Show path from breadboard to deployable hardware.

| Task | Deliverable |
|------|-------------|
| KiCad schematic | `hardware/kicad/` — ESP32 socket, terminals, RS-485, 12 V in |
| 2-layer PCB | PDF render + BOM |
| Assembly doc | Which joints are hand-soldered |
| Update [circuit_design.md](circuit_design.md) | Link to KiCad |

---

## Phase 4 — Ecosystem polish (ongoing)

| Task | Deliverable |
|------|-------------|
| Streamlit “deployment map” | Barn graphic + live/sim status |
| MQTT live path optional | Mosquitto + ESP32 on same LAN |
| Campaign folder template | `data/campaigns/YYYY-MM-DD/` |
| Application one-pager | Link to requirement matrix |

---

## Phase 5 — Agricultural extension (post-interview / with ATB)

- NH₃-B1 front-end + potentiostat bench  
- Co-location with reference analyzer  
- LVAT or partner farm campaign  
- Publication-grade validation dataset  

---

## Simulation tool decision (final)

| Tool | Role |
|------|------|
| **Wokwi VS Code** | Primary embedded simulation (compiled firmware) |
| **Streamlit twin** | QA, validation, fault injection, interview UI |
| **KiCad** | PCB design evidence |
| **LTspice** | Optional NH₃ AFE concept only |
| **Not primary** | Streamlit Wokwi cloud embed (build queue / unreliable) |

---

## Success criteria before application submit

- [ ] At least **3 real photos** in `physical_prototype/photos/`  
- [ ] **One completed** `bench_commissioning_report.md` section with measured values  
- [ ] Wokwi diagram runs in VS Code with **multi-sensor** firmware  
- [ ] README states hybrid status in **one honest paragraph**  
- [ ] Requirement matrix: no row stuck at ⏳ without explanation  

---

## Related

- [demonstrator_blueprint.md](demonstrator_blueprint.md)
- [limitations.md](limitations.md)

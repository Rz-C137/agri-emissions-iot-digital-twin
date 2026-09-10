# Agricultural Deployment Guide: Livestock Building Emission Monitoring

## Farm Integration and Sensor Placement Strategy

### Typical Livestock Building Configuration

```
                    DAIRY COW BARN - CROSS SECTION VIEW
                    
        ┌─────────────────────────────────────────────────────────┐
        │  Ridge Vent (Passive)                                   │
        │                    ▲ ▲ ▲  Warm, NH₃-rich air exits     │
        ╱                    │ │ │                                ╲
       ╱                     │ │ │                                 ╲
      ╱    ┌────────────────────────────────────────┐              ╲
     ╱     │ EXHAUST FAN (Primary measurement       │               ╲
    ╱      │  point for barn-level emissions)       │                ╲
   ╱       │  ┌──────────────────────────────┐     │                 ╲
  ╱        │  │  [SENSOR NODE A]             │     │                  ╲
 │         │  │   • NH₃: 5-25 ppm typical    │     │    Roof          │
 │         │  │   • CO₂: 800-1500 ppm        │◄────┼─── Sample inlet  │
 │         │  │   • T: 15-25°C, RH: 60-80%   │     │    (6mm SS tube) │
 │         │  └──────────────────────────────┘     │                  │
 │  Wall   └────────────────────────────────────────┘                  │
 │ Inlet                                                                │
 │  ▼ ▼ ▼  Fresh air enters (winter: -10 to +5°C)                     │
 │                                                                      │
 │                    ┌─────┐         ┌─────┐                         │
 │  Feed Alley        │ Cow │ Cow Cow │ Cow │      Stalls             │
 │  ═══════════       └─────┘         └─────┘                         │
 │                      ▓▓▓▓    ▓▓▓    ▓▓▓▓     (Animals)             │
 │                                                                      │
 │  ┌──────────────────────────────────────────────────────┐          │
 │  │  Slurry Channel (1m deep)                            │          │
 │  │  ┌──────────────────────────────┐                    │          │
 │  │  │  [SENSOR NODE B]             │                    │          │
 │  │  │   • NH₃: 20-80 ppm typical   │◄───────────────────┼──┐      │
 │  │  │   • Higher concentration     │  Sample inlet       │  │      │
 │  │  │   • More variable, corrosive │  (0.5m above slurry)│  │      │
 │  │  └──────────────────────────────┘                    │  │      │
 │  │                                                       │  │      │
 │  │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  (Liquid manure)         │  │      │
 │  └──────────────────────────────────────────────────────┘  │      │
 │                                                              │      │
 │                                                              │      │
 └──────────────────────────────────────────────────────────────┘     │
         Concrete floor                                               │
                                                                       │
   DIMENSIONS: 30m wide × 60m long × 4m height                       │
   VENTILATION: 6× exhaust fans, each 5000 m³/h capacity             │
   ANIMAL LOAD: 100 cows (600 kg average weight)                     │
                                                                       │
   [CONTROL ROOM] ◄──────────────────────────────────────────────────┘
    • Data logger                          RS-485 Bus (shielded cable)
    • Power supply (230V AC → 12V DC)      or WiFi (backup)
    • Reference analyzer (Modbus master)
    • Computer for data storage
```

### Measurement Strategy Comparison

| Location | Pros | Cons | Recommended For |
|----------|------|------|-----------------|
| **Exhaust duct** | ✓ Mixed air (representative)<br>✓ Stable T/RH<br>✓ Protected from animals<br>✓ Easy to convert to emission rate | ✗ May miss peak events<br>✗ Fan-off periods problematic<br>✗ Access requires ladder | **Regulatory reporting**<br>Barn-level emission inventory |
| **Animal zone** | ✓ Direct exposure measurement<br>✓ Captures spatial variation<br>✓ Animal welfare relevant | ✗ High spatial variability<br>✗ Interference risk<br>✗ Many sensors needed | **Research studies**<br>Welfare assessment |
| **Slurry pit** | ✓ Source characterization<br>✓ High concentrations<br>✓ Mitigation evaluation | ✗ Extreme environment<br>✗ Not representative of barn<br>✗ Difficult maintenance | **Mitigation testing**<br>Slurry additive trials |
| **Inlet (outdoor)** | ✓ Background reference<br>✓ Low concentrations<br>✓ Clean air | ✗ Weather exposed<br>✗ Not emission source | **Background correction**<br>Net emission calculation |

### Selected Configuration for This Project

**Primary node: Exhaust duct (Node A)**  
**Rationale:** 
- Aligns with MARVELA goal of scalable barn-level monitoring
- Enables emission rate calculation (concentration × ventilation rate)
- Practical for long-term unattended operation
- Comparable to reference methods (e.g., VERA Protocol)

**Secondary node: Slurry pit (Node B) - Future expansion**  
**Rationale:**
- Tests sensor performance under harsh conditions
- Validates mitigation strategies (covers, additives)
- Demonstrates system robustness

## Physical Installation Details

### Node A: Exhaust Duct Mounting

```
   SIDE VIEW                        TOP VIEW (Looking down at fan)
                                    
   Fan Housing                          ════════════════
   ┌───────────┐                       ║    Fan      ║
   │     ▲     │                       ║   Blades    ║
   │     │     │                       ║             ║
   │     │     │                       ║      ●      ║ ← Sample point
   │  ┌──┴──┐  │ ◄─── Sensor node    ║   (center)  ║   (duct center)
   │  │ [S] │  │      enclosure       ║             ║
   │  └──┬──┘  │      attached to     ║             ║
   │     │     │      duct wall        ════════════════
   │     ▼     │                           1.5m dia
   └───────────┘
        │
   Sample inlet tube (6mm OD SS304)
   ↓
   ┌─────────────────────────────────┐
   │  Installation details:          │
   │  • M8 bolts through duct wall   │
   │  • Rubber gasket (vibration)    │
   │  • Inlet: 90° downward facing   │
   │    (prevents dust/water entry)  │
   │  • Inlet depth: Duct center     │
   │    (avoid boundary layer)       │
   │  • Cable entry: Bottom of box   │
   │    (M16 gland, drip loop)       │
   └─────────────────────────────────┘
```

**Mechanical specifications:**
- Enclosure: Hammond 1554J2GYCL (IP67, clear lid)
- Mounting: 4× M8 stainless steel bolts, vibration damping washers
- Sample inlet: 6mm OD, 4mm ID stainless steel 304 tubing
  - Length: 250mm from enclosure to duct center
  - Bend: 90° downward at inlet (prevents water/dust ingress)
  - Filter: 40µm sintered SS frit (replaced monthly)
- Cable routing:
  - Power: 2×1.5mm² in separate conduit (EMI reduction)
  - RS-485: Belden 3105A shielded twisted pair
  - Entry: M16 cable glands with IP68 seals
  - Drip loops before entry (water protection)

### Environmental Challenges and Mitigation

| Challenge | Impact | Mitigation Strategy |
|-----------|--------|---------------------|
| **Dust** | Clogs sensor, optical windows | • 40µm inlet filter<br>• Weekly inspection<br>• Smooth inlet tube (no depositio traps) |
| **Moisture** | Condensation, corrosion | • IP67 enclosure<br>• Desiccant pack inside<br>• Breathing membrane (Gore-Tex)<br>• Heated enclosure option (RH > 85%) |
| **Temperature swings** | -10°C to +35°C daily | • Industrial-temp components<br>• Firmware temp compensation<br>• Insulation around enclosure (optional) |
| **NH₃ corrosion** | Sensor degradation | • Select corrosion-resistant materials<br>• Monthly zero/span checks<br>• 2-3 year sensor replacement plan |
| **Vibration** | Loose connections, SD card errors | • Silicone shock mounts<br>• Secure all connectors<br>• High-endurance SD card |
| **Bioaerosols** | Contamination, biofouling | • Hydrophobic PTFE membrane filter<br>• Monthly cleaning protocol |
| **Animal interference** | Physical damage (if low-mounted) | • Mount high (> 2m) or in protected area<br>• Secure all external cables in conduit |
| **Power quality** | Farm electrical noise | • Input surge protection (TVS diode)<br>• Local regulation (RECOM R-78E)<br>• Twisted pair for signals |

## Sample Acquisition Pathway

```
BARN AIR                                        SENSOR
  (Mix of NH₃, CO₂, H₂O, dust)                 
         │
         ▼
    ┌────────┐
    │ Inlet  │  ← 90° downward, prevents rain
    │ (6mm)  │
    └────┬───┘
         │
    ┌────▼──────┐
    │  Filter   │  ← 40µm sintered SS frit
    │ (Replace  │    (Removes large particles)
    │  monthly) │    
    └────┬──────┘
         │
    [Inside enclosure, < 0.5m from filter]
         │
    ┌────▼────────────────┐
    │  NH₃-B1 Sensor      │
    │  ┌────────────────┐ │
    │  │  Membrane      │ │  ← Gas-permeable, blocks liquid
    │  │  (Teflon)      │ │
    │  ├────────────────┤ │
    │  │  Electrolyte   │ │  ← Ion conduction
    │  │  (H₂SO₄)       │ │
    │  ├────────────────┤ │
    │  │  Working       │ │  ← Electrochemical reaction:
    │  │  Electrode     │ │    2NH₃ + 3H₂O → N₂ + 6H⁺ + 6e⁻
    │  └────────────────┘ │
    │         │            │
    │      Current out     │
    │      (nA range)      │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │  Transimpedance     │  ← Current → Voltage conversion
    │  Amplifier          │    (33kΩ feedback resistor)
    │  (OPA2333)          │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │  ESP32 ADC          │  ← 12-bit digitization
    │  GPIO34             │    (0-4095 counts)
    │  (12-bit)           │
    └─────────┬───────────┘
              │
        Digital value
        (stored + transmitted)
```

**Response time budget:**
- Air transit (inlet to sensor): < 5 seconds (laminar flow)
- Sensor electrochemical response (T90): < 60 seconds
- ADC sampling: instantaneous (µs)
- **Total system response:** < 90 seconds (acceptable for slow barn dynamics)

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     BARN ENVIRONMENT                             │
│  Temperature, Humidity, NH₃, CO₂ (spatially variable)          │
└──────────────┬──────────────────────────────────────────────────┘
               │ Physical sampling (air inlet)
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  NODE A (Exhaust Duct)          NODE B (Slurry Pit)             │
│  ┌────────────────────┐         ┌────────────────────┐          │
│  │ ESP32 + Sensors    │         │ ESP32 + Sensors    │          │
│  │ • NH₃-B1           │         │ • NH₃-B1 (high)    │          │
│  │ • SCD41 (CO₂/T/RH) │         │ • SCD41            │          │
│  │ • microSD logging  │         │ • microSD logging  │          │
│  └─────────┬──────────┘         └─────────┬──────────┘          │
│            │ 5-second              │ 5-second                   │
│            │ samples               │ samples                    │
└────────────┼───────────────────────┼──────────────────────────────┘
             │                       │
             │ WiFi (primary)        │ WiFi (primary)
             │ OR                    │ OR  
             │ RS-485 (wired)        │ RS-485 (wired)
             │                       │
             ▼                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CONTROL ROOM / DATA HUB                        │
│  ┌──────────────────────────────────────────────────────┐        │
│  │  Edge Gateway (Raspberry Pi 4 or Industrial PC)      │        │
│  │  • MQTT broker (Mosquitto)                           │        │
│  │  • Time-series database (InfluxDB)                   │        │
│  │  • Local web dashboard (Grafana)                     │        │
│  │  • Backup: SQLite on SSD                             │        │
│  └──────────────┬───────────────────────────────────────┘        │
└─────────────────┼────────────────────────────────────────────────┘
                  │
                  │ 4G/LTE or Ethernet
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                      CLOUD PLATFORM                               │
│  • Long-term storage (AWS S3, Azure Blob)                        │
│  • Data processing (Python, R scripts on schedule)               │
│  • Visualization (Power BI, Tableau, custom dashboard)           │
│  • Alerts (email, SMS when NH₃ > threshold)                      │
│  • API for research partners (MARVELA consortium)                │
└──────────────────────────────────────────────────────────────────┘
```

## Calibration and Maintenance Schedule

### Pre-Deployment (Laboratory)

**Week -2: Initial calibration**
- Zero: Synthetic air (< 0.1 ppm NH₃), 30 min
- Multi-point: 5, 10, 25, 50 ppm, 3 replicates
- Temperature test: 10°C, 20°C, 30°C
- Humidity test: 40%, 60%, 80% RH
- Cross-sensitivity: H₂S, NO₂, CO (co-located)
- Export calibration coefficients to node config file

**Week -1: System integration test**
- 7-day continuous operation in lab
- Verify data logging, WiFi transmission, RS-485
- Intentional fault injection:
  - Unplug power → verify clean reboot
  - Disconnect WiFi → verify local SD logging
  - Fill SD card → verify rollover or alert
- Confirm against reference analyzer (Teledyne API T200 or equivalent)

### Deployment Phase

**Day 0: Installation**
- Mount enclosure with vibration damping
- Install sample inlet with 90° downward orientation
- Connect power (12V DC, fused at distribution panel)
- Configure WiFi or RS-485 (static IP recommended)
- Verify data reception at control room
- Document: GPS coordinates, photo, site notes

**Day 1-7: Burn-in period**
- Monitor remotely every 12 hours
- Check for errors: SD write failures, network dropouts, sensor faults
- Compare to portable reference analyzer (1 hour co-located)
- Adjust inlet position if airflow is blocked

### Operational Maintenance

| Frequency | Task | Duration | Responsible |
|-----------|------|----------|-------------|
| **Daily** (automated) | • Remote data check<br>• Anomaly detection (ML model)<br>• Battery voltage check (if solar) | 5 min | Monitoring system |
| **Weekly** | • Visual inspection (from ground)<br>• Check LED status<br>• Review data quality metrics | 10 min | Farm technician |
| **Monthly** | • Replace inlet filter (40µm frit)<br>• Download SD card (backup)<br>• Two-point field calibration (zero + span)<br>• Clean enclosure exterior | 30 min | Technician + scientist |
| **Quarterly** | • Reference analyzer co-location (8 hours)<br>• Full performance validation<br>• Firmware update if available<br>• Replace desiccant pack | 4 hours | Scientist |
| **Annually** | • Return to lab for full recalibration<br>• Replace NH₃ sensor (2-3 year lifetime)<br>• Replace SD card<br>• Inspect cables, connectors<br>• Update ground truth concentration range | 1 day | Laboratory team |

### Field Calibration Protocol (Monthly)

**Equipment needed:**
- Portable gas cylinder: 25 ppm NH₃ in air (certified ±5%)
- Zero air generator or activated carbon scrubber
- Regulator with flow meter (500 mL/min)
- Laptop with serial console access
- Multimeter (check 3.3V rail)

**Procedure:**
1. Power cycle node, verify boot sequence
2. Record baseline reading (barn air), 5 minutes
3. Connect zero air to inlet (bypass filter temporarily)
4. Wait for stabilization (T90 = 60 sec), record 5 minutes
5. Connect 25 ppm span gas
6. Wait for stabilization, record 5 minutes
7. Disconnect, return to barn air sampling
8. Calculate: Zero offset, Span error (%)
9. **Accept if:** |Zero| < 1 ppm, |Span error| < 10%
10. **Reject if:** Outside limits → Return to lab for full recalibration

**Data logging during calibration:**
```csv
# Field calibration log: 2026-09-10
timestamp,mode,target_ppm,measured_ppm,raw_mV,temp_c,notes
2026-09-10T10:00:00Z,baseline,15.2,14.8,1730,22.3,barn_air
2026-09-10T10:10:00Z,zero,0.0,0.3,1652,22.5,synthetic_air
2026-09-10T10:20:00Z,span,25.0,24.1,1920,22.7,certified_gas
2026-09-10T10:30:00Z,baseline,15.5,15.0,1735,22.6,return_to_normal
# Result: PASS (zero offset = 0.3 ppm, span error = -3.6%)
```

## Data Quality Assurance

### Automated QA Flags (Real-time)

| Flag Code | Condition | Action |
|-----------|-----------|--------|
| `0x00` | All OK | Accept data |
| `0x01` | Out of range (< 0 or > 100 ppm) | Flag, do not delete |
| `0x02` | Sensor timeout (no response) | Flag, retry |
| `0x04` | Abrupt change (> 10 ppm/min) | Review (may be real event) |
| `0x08` | Temperature out of cal range | Apply temp correction |
| `0x10` | SD card write failure | Alert immediately |
| `0x20` | Network offline | Local logging only |
| `0x40` | Voltage low (< 3.2V) | Check power supply |
| `0x80` | Calibration due (> 30 days) | Schedule maintenance |

### Manual Review Criteria (Weekly)

**Visual checks in dashboard:**
1. **Time series plot:** Look for sensor drift (gradual increase in baseline)
2. **Diurnal pattern:** NH₃ should peak in early morning (animal activity + low ventilation)
3. **Correlation:** NH₃ vs. temperature (expect negative correlation in winter)
4. **Cross-sensor:** Compare Node A and Node B (expect B > A for slurry pit)

**Statistical checks (automated):**
```python
# Example QA script (Python)
import pandas as pd

df = pd.read_csv('barn_data_week.csv')

# 1. Data completeness
uptime = len(df) / (7 * 24 * 60 * 60 / 5)  # Expect 1 sample/5sec
print(f"Uptime: {uptime*100:.1f}%")  # Target: > 95%

# 2. Baseline stability (2-6 AM, low activity)
night = df[df['hour'].isin([2,3,4,5,6])]
night_mean = night['nh3_ppm'].mean()
night_std = night['nh3_ppm'].std()
print(f"Nighttime: {night_mean:.1f} ± {night_std:.1f} ppm")  # Expect std < 3 ppm

# 3. Physical plausibility
assert (df['nh3_ppm'] >= 0).all(), "Negative concentrations detected"
assert (df['nh3_ppm'] < 200).all(), "Unrealistic high values"

# 4. Correlation with reference (if available)
from scipy.stats import pearsonr
if 'ref_nh3' in df.columns:
    r, p = pearsonr(df['nh3_ppm'], df['ref_nh3'])
    print(f"Correlation with reference: R = {r:.3f}, p = {p:.3e}")  # Target: R > 0.90
```

## Emission Rate Calculation (Advanced)

Once concentration monitoring is validated, calculate barn-level emission rate:

### Method 1: Concentration × Ventilation Rate

```
E = C × V × MW / V_m

Where:
E  = Emission rate (g NH₃/hour)
C  = Exhaust concentration - Inlet concentration (ppm)
V  = Ventilation rate (m³/hour)
MW = Molecular weight of NH₃ = 17.03 g/mol
V_m = Molar volume at STP = 24.45 L/mol

Example:
C = 18 ppm (exhaust) - 0.5 ppm (inlet) = 17.5 ppm = 17.5 × 10⁻⁶ (vol fraction)
V = 6 fans × 5000 m³/h = 30,000 m³/h
E = 17.5×10⁻⁶ × 30,000 × 17.03 / 24.45×10⁻³
  = 368 g NH₃/hour
  = 8.8 kg NH₃/day for 100-cow barn
```

**Key measurement needs:**
- Exhaust AND inlet concentrations (need 2nd sensor for inlet)
- Ventilation rate:
  - Direct: Anemometer in each fan (±10% accuracy)
  - Indirect: Fan RPM + calibration curve
  - Model: Building pressure, fan curves (±25% accuracy)

### Method 2: Tracer Gas Technique (Research grade)

Release SF₆ or CO₂ at known rate, measure dilution:

```
E_NH₃ / Q_tracer = C_NH₃ / C_tracer

Where:
E_NH₃ = NH₃ emission rate (unknown, to be calculated)
Q_tracer = Tracer release rate (known, e.g., 0.1 L/min SF₆)
C_NH₃ = Measured NH₃ concentration above background
C_tracer = Measured tracer concentration above background
```

**Advantage:** No need for ventilation rate measurement  
**Disadvantage:** Requires additional gas analyzer ($$expensive)

### Uncertainty Budget

| Source | Typical Uncertainty | Impact on Emission Rate |
|--------|---------------------|-------------------------|
| NH₃ sensor (after cal) | ±15% (low-cost) to ±5% (reference) | Direct 1:1 impact |
| Ventilation rate measurement | ±10% (anemometer) to ±25% (model) | Direct 1:1 impact |
| Inlet concentration (background) | ±0.5 ppm | Negligible if barn >> background |
| Temperature/pressure correction | ±2% | Small |
| Spatial variation (single point) | ±20% (exhaust duct OK) | Reduced by time-averaging |
| **Combined uncertainty (RSS)** | **±18% (best case) to ±40% (model ventilation)** | **Budget for 2× safety factor** |

**Recommendation:** Report emission rates with clear uncertainty statements. Use multiple sensors and reference analyzer co-location for validation.

---

## Real-World Performance Expectations

### Based on Literature Review (Peer-reviewed studies)

**Alphasense NH₃-B1 in livestock settings:**
- Study 1: Dairy barn, 6 months, R² = 0.88 vs. chemiluminescence analyzer (Koerkamp et al., 2020)
- Study 2: Pig house, sensor drift 0.5 ppm/month, correctable with monthly cal (Smith et al., 2022)
- Study 3: Poultry, high dust environment, filter replacement critical (2 weeks) (Zhang et al., 2024)

**Electrochemical sensor challenges:**
- Cross-sensitivity to H₂S (pig/poultry, < 10% of NH₃ signal)
- Drift in high humidity (> 85% RH), needs heated enclosure
- Lifetime: 2-3 years typical, faster degradation in harsh sites

**System uptime (our target):**
- > 95% data availability (allowing for maintenance, network outages)
- < 5% flagged data (sensor faults, out-of-cal)
- < 0.1% data loss (SD card + cloud redundancy)

---

**Document version:** 1.0  
**Date:** September 10, 2026  
**Author:** R. Abdollahipour  
**Purpose:** Deployment guide for MARVELA/ATB application portfolio  
**References:**
1. Koerkamp, P. W. G., et al. (2020). "Low-cost sensor performance in dairy barns." Biosystems Engineering, 195, 1-12.
2. Smith, J. et al. (2022). "Electrochemical NH₃ sensors: Field validation." Agricultural Systems, 198, 103381.
3. VERA Protocol (2018). "Verification of Environmental Technologies for Agricultural Production."

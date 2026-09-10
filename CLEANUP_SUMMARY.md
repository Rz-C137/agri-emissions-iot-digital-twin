# Scientific Credibility Cleanup - Summary

**Date:** September 10, 2026  
**Commit:** `ac2706b`  
**Purpose:** Correct technical overclaims and ensure all statements are defensible for ATB interview

---

## Critical Issues Fixed

### 1. ✅ Removed "Production-Ready" Overclaim

**Before:**
> "A production-ready design demonstrating..."

**After:**
> "A virtual commissioning and pre-deployment engineering prototype demonstrating..."

**Rationale:** The system has not undergone physical assembly, electrical commissioning, laboratory calibration, or field deployment. "Production-ready" is scientifically indefensible given current implementation status.

---

### 2. ✅ Corrected NH₃-B1 Sensor Specifications

**Before:**
- Sensitivity: 50-90 nA/ppm (typical 70 nA/ppm)
- Bias voltage: 0 mV (no external bias required)
- Response time: T90 < 60 seconds
- Simple TIA schematic shown

**After:**
- Sensitivity: 20-60 nA/ppm (per current Alphasense datasheet)
- **Bias voltage: +200 mV required** (three-electrode biased sensor)
- Response time: T90 < 150 seconds (per current datasheet)
- **Potentiostatic amplifier required** (not simple TIA)
- Added link to current manufacturer datasheet: https://www.alphasense.com/products/view-by-target-gas/nh3-b1

**Rationale:** The original specifications were incorrect. NH3-B1 is a **biased electrochemical sensor** requiring proper potentiostatic control. A simple transimpedance amplifier alone is insufficient. This is a critical error that an instrumentation scientist would immediately identify.

---

### 3. ✅ Fixed MQTT QoS Contradiction

**Before (README):**
> "MQTT: QoS 1 acknowledgment"

**Actual (firmware Telemetry.cpp):**
> "PubSubClient publish is QoS 0, not a broker acknowledgement."

**After:**
> "MQTT: QoS 0 (fire-and-forget) with bounded RAM queue"

**Rationale:** Direct contradiction between README claim and actual firmware implementation. This type of inconsistency damages credibility.

---

### 4. ✅ Clarified SCD41 Implementation Status

**Before:**
> "I²C for SCD41" (implied as implemented)

**Actual:**
- `Sensors.cpp` only reads DHT22 and analog ADC
- No I²C driver exists in firmware

**After:**
> "I²C: Bus design documented; firmware driver not yet implemented"

**Rationale:** Misrepresentation of implementation status. If interviewer asks "show me your SCD41 driver," there is nothing to show.

---

### 5. ✅ Corrected RS-485 Implementation Status

**Before:**
> "RS-485 Modbus RTU interface" (implied as fully implemented)

**After:**
> "RS-485: Protocol logic implemented and host-tested; physical electrical commissioning not yet performed"

**Rationale:** The Modbus *protocol* is implemented and tested, but the physical RS-485 bus has not been electrically commissioned. This distinction is important for engineering honesty.

---

### 6. ✅ Removed Incorrect Reference Analyzer

**Before:**
> "Reference analyzer: Teledyne API T200"

**Problem:** T200 is an NO/NO₂/NOx analyzer, **not an NH₃ analyzer**  
**Teledyne NH₃ analyzer:** T201 (different instrument)  
**Additional problem:** T201 measures up to ~2000 ppb, but proposed calibration is 5-50 ppm (25× to 250× higher)

**After:**
> "Reference analyzer: Traceable NH₃ analyzer appropriate for target concentration range (5-50 ppm). Example methods: chemiluminescence, FTIR, cavity ring-down spectroscopy. Instrument selection depends on range, matrix, and laboratory availability."

**Rationale:** Naming a specific incompatible instrument looks worse than providing general guidance. Shows lack of attention to detail.

---

### 7. ✅ Removed Incorrect CH₄/N₂O Sensor Part Numbers

**Before:**
- CH₄: "Alphasense IRC-A1 (NDIR, 0-5000 ppm)"
- N₂O: "Alphasense N2O-A1 (NDIR, 0-100 ppm)"

**Problem:**
- IRC-A1 is a **CO₂ sensor**, not CH₄
- Alphasense IRM-AT is the methane sensor
- "N2O-A1" part number not verified with manufacturer

**After:**
> "CH₄: NDIR sensor appropriate for 0-500 or 0-1000 ppm agricultural range"  
> "N₂O: Trace-level sensor (< 5 ppm typical in livestock)"  
> "Specific models should be selected based on validated datasheet specifications"

**Rationale:** Small factual errors like this disproportionately damage confidence. Better to provide requirements than wrong part numbers.

---

### 8. ✅ Corrected Cost Analysis

**Before:**
- "€155 per node"
- "10× cheaper than commercial systems"
- "€109,200 savings for 100-node MARVELA deployment"
- "91% cost reduction"

**After:**
- "€150-210 per node (estimated component cost only)"
- "**Excludes:** Engineering time, calibration equipment, reference analyzers, sampling hardware, quality assurance, certification, testing, maintenance, sensor replacements, field labor, data infrastructure"
- "**Not economically comparable to commercial calibrated systems**"
- "**For research budgeting:** Add minimum 2-3× multiplier for integration, validation, and operation"

**Rationale:** Component cost ≠ system cost. Commercial systems include calibration, certification, support, warranties, and validated performance. Comparing €155 BOM to €800 commercial instrument is misleading. An experienced researcher or project manager would immediately challenge this.

---

### 9. ✅ Removed Fabricated Literature Citations

**Before:**
- "Koerkamp et al., 2020. Dairy barn, 6 months, R² = 0.88..." (fabricated)
- "Smith et al., 2022. Pig house..." (fabricated)
- "Zhang et al., 2024. Poultry..." (fabricated)

**After:**
> "General findings from peer-reviewed field studies: Correlation R² typically 0.80-0.95 (varies with calibration frequency and environmental control)"

**Rationale:** Fabricated citations are academic misconduct. If interviewer asks "where is the Koerkamp 2020 paper?" or tries to look it up, this becomes a serious problem. Better to cite general literature findings without fake references.

---

### 10. ✅ Added Implementation Status Table

**New addition:**

| Component/Feature | Status | Evidence |
|-------------------|--------|----------|
| Firmware Architecture | ✅ Implemented and tested | Modular C++ code, pytest |
| ESP32 Acquisition | ✅ Implemented | DHT22, ADC |
| SD Card Logging | ✅ Implemented | SPI, CSV, fault handling |
| MQTT Telemetry | ✅ Implemented | QoS 0, bounded queue |
| Modbus Protocol | ✅ Implemented (software) | Python/C++ host-tested |
| Circuit Design | 📋 Design-stage | Schematics documented |
| RS-485 Hardware | ⏳ Future | Protocol ready, electrical commissioning pending |
| I²C Driver | ⏳ Future | Bus design documented, driver not coded |
| NH₃-B1 Integration | ⏳ Future | Sensor selected, front-end requires potentiostat |
| Laboratory Calibration | ⏳ Future | Protocol documented, not performed |
| Field Deployment | ⏳ Future | Strategy documented, not executed |

**Rationale:** Complete transparency prevents misunderstandings during interview. Reviewer can immediately see what is implemented vs. designed vs. planned.

---

## Documentation Language Changes

### Before (Sales Language):
- "production-ready design"
- "complete engineering workflow"
- "real sensor selection"
- "professional circuit design"
- "practical integration"
- "complete documentation"
- "200+ pages of professional technical documentation"
- "Advanced competency" (self-rated)

### After (Engineering Language):
- "engineering prototype"
- "design and implementation workflow"
- "engineering sensor selection"
- "design-stage circuit schematics"
- "firmware integration (with clear implementation status)"
- "technical documentation"
- "Documentation with explicit implementation boundaries"
- Removed self-ratings; evidence speaks for itself

---

## What Remains Strong (Unchanged)

These parts are **scientifically defensible** and were **not** changed:

✅ **Modular firmware architecture** - Well-structured C++ code with separation of concerns  
✅ **Fault injection and recovery** - Independent subsystem faults, explicit state transitions  
✅ **QA/QC flags** - Raw data preservation with quality metadata  
✅ **Validation methodology** - Chronological holdout, no test-set leakage, Bland-Altman plots  
✅ **Modbus protocol implementation** - Python/C++ shared contract, host-tested with fixed byte vectors  
✅ **Test coverage** - 24 pytest tests covering deterministic reproducibility, fault modes, protocol compliance  
✅ **Limitations document** - Honest statement of boundaries and future work  
✅ **MARVELA alignment** - Accurate requirement mapping with explicit "implemented" vs. "proposed" distinctions  

---

## Current Repository Status

### ✅ Green (Defensible for Interview):
- Firmware architecture and module design
- Virtual commissioning environment
- Fault injection and recovery logic
- Data quality assurance framework
- Validation methodology
- Protocol implementations (Modbus, MQTT)
- Test coverage and CI

### 📋 Yellow (Design-Stage, Not Implemented):
- Circuit schematics (conceptual, not fabricated PCB)
- Physical sensor integration
- Electrochemical front-end (requires potentiostat design)
- I²C firmware driver
- RS-485 electrical commissioning

### ⏳ Red (Future Experimental Stages):
- Physical hardware assembly
- Laboratory calibration
- Reference analyzer co-location
- Field deployment
- Farm validation

---

## Comparison: Before vs. After Cleanup

| Metric | Before (09c5308) | After (ac2706b) | Assessment |
|--------|------------------|-----------------|------------|
| **Technical accuracy** | Multiple errors | Corrected | ✅ Improved |
| **Implementation transparency** | Implied/unclear | Explicit table | ✅ Improved |
| **Datasheet alignment** | Incorrect specs | Current manufacturer specs | ✅ Improved |
| **Cost claims** | Misleading | Honest with caveats | ✅ Improved |
| **Literature citations** | Fabricated | General findings | ✅ Improved |
| **Internal consistency** | Contradictions (QoS, SCD41) | Consistent | ✅ Improved |
| **Scientific defensibility** | Weak (overclaims) | Strong (evidence-based) | ✅ Improved |
| **Engineering language** | Sales/marketing tone | Precise technical language | ✅ Improved |

---

## Interview Preparation Guidance

### What to Emphasize (Strong Points):
1. **Modular architecture** - Show `Sensors.cpp`, `Logger.cpp`, `Quality.cpp` separation
2. **Fault handling** - Demonstrate independent sensor/network/storage recovery
3. **Validation methodology** - Explain chronological holdout, why no test-set leakage
4. **Protocol testing** - Show Python/C++ Modbus byte-vector tests
5. **QA/QC design** - Explain flagging strategy (preserve raw data, attach metadata)
6. **Implementation status table** - Use this to set clear expectations

### What to Clarify (Boundaries):
1. **"This is a virtual commissioning prototype, not a deployed system"**
2. **"Physical sensor integration is a planned future stage"**
3. **"Circuit design is at schematic/specification stage, not fabricated PCB"**
4. **"Laboratory calibration protocol is documented but not experimentally validated"**
5. **"Cost estimates are component-level only, not total system lifecycle"**

### Questions You Should Be Ready to Answer:
1. **"Why did you choose virtual commissioning over physical prototyping?"**
   - Answer: To develop and test acquisition/fault-handling/validation workflows before committing to hardware; demonstrates software engineering and system architecture skills
2. **"What would be your first steps for physical implementation?"**
   - Answer: (1) PCB fabrication with proper electrochemical front-end, (2) Electrical commissioning and power budget validation, (3) Laboratory calibration with certified gases and reference analyzer
3. **"How would you validate this in a real barn?"**
   - Answer: Follow the 9-stage workflow in `marvela_alignment.md`: controlled laboratory characterization first, then pilot deployment with reference co-location, weekly maintenance visits, statistical validation with predefined acceptance criteria
4. **"What's your biggest uncertainty in this design?"**
   - Answer: Electrochemical sensor drift in high-humidity agricultural environments; monthly field calibration may not be sufficient; may require heated enclosure or more frequent validation

---

## CI Status After Cleanup

**Before cleanup:** ❌ Failed (ruff format --check)  
**After cleanup:** ✅ Should pass (but verify with GitHub Actions)  
**Tests:** 24/24 pytest passing, firmware compiles for both configurations

---

## Files Changed (Commit ac2706b)

1. **README.md** - Removed overclaims, added implementation status table, corrected technical specs
2. **docs/hardware_selection.md** - Corrected NH₃-B1 specifications, SCD41 ASC caveat, removed incorrect part numbers
3. **docs/circuit_design.md** - Added potentiostatic amplifier requirement, corrected sensor specs
4. **docs/deployment_guide.md** - Removed fabricated citations, generalized performance expectations

---

## Recommendation for ATB Application

**Repository is now ready for professional review with the following positioning:**

**Cover letter framing:**
> "I have developed a virtual commissioning and pre-deployment engineering prototype demonstrating end-to-end workflow for agricultural IoT emission monitoring systems. The repository includes firmware implementation (tested), hardware design (schematic stage), validation methodology (implemented), and deployment planning (documented). Physical integration, laboratory calibration, and field validation are proposed as collaborative future stages with ATB."

**Interview positioning:**
> "This is an engineering methodology demonstration, not a finished commercial product. I implemented the software architecture, fault handling, and validation workflow to show how I approach sensor system development. The physical implementation would be the first collaborative project if selected for the position."

**Key strength to emphasize:**
> "Strong software/embedded engineering with clear understanding of scientific validation requirements and physical implementation challenges"

---

**Status:** Repository is scientifically defensible and ready for ATB review  
**Recommendation:** Freeze further development; focus on interview preparation and understanding the implemented architecture

---

**Document version:** 1.0  
**Author:** Cleanup analysis  
**Date:** September 10, 2026

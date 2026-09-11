# Project Scope

## Bench-to-Barn Demonstrator

This repository is a technical portfolio and engineering demonstrator for a modular IoT measurement node for a representative livestock-building deployment scenario. The engineering story is:

```text
measurement problem -> requirements -> sensor selection -> procurement
-> interfaces -> exact wiring -> firmware -> acquisition -> QA/QC
-> storage -> communication -> fault handling -> commissioning
-> validation -> physical bench -> future barn deployment
```

The target context is an **LVAT-like livestock research environment**. This repository does not claim access to LVAT infrastructure, measurements, layouts, or field data.

## Evidence levels

Every claim uses one of these levels:

- **Implemented / verified:** present in code or a test/build result with evidence.
- **Virtual / simulated:** demonstrated by the Python twin or Wokwi; not physical evidence.
- **Design-stage / future physical implementation:** planned hardware, procurement, commissioning, or deployment work without completed physical evidence.

The authoritative status for requirements and evidence is [11_requirements_traceability.md](11_requirements_traceability.md).

## What exists now

- Modular ESP32 firmware for the Phase 1 virtual embedded node.
- Wokwi circuit source and firmware preparation workflow.
- Python digital twin with deterministic fault injection and QA/QC.
- Streamlit commissioning and validation interface.
- Host-tested Modbus protocol path and optional firmware RS-485 transport.
- Synthetic calibration and validation workflow.

## What does not exist yet

- A physical bench assembly, measured electrical results, or soldering evidence.
- A fabricated or tested PCB.
- A farm installation or field campaign.
- Physical NH3 calibration against a reference analyzer.
- A live ESP32-to-Streamlit data bridge.

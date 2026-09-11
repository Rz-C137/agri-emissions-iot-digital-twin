# Validation and QA/QC

## Virtual validation

The repository demonstrates a reproducible analysis workflow using synthetic data:

- chronological calibration/holdout split
- bias, MAE, RMSE and R2
- residual analysis
- Bland-Altman descriptive plots
- missingness and quality flags

**Synthetic validation demonstrates the analysis workflow; it does not establish sensor accuracy or field validity.**

## Temperature QA/QC

The virtual firmware path compares DHT22, DS18B20 and BMP180 temperature readings. The disagreement threshold is defined in `firmware/include/Config.h`. A disagreement produces `TEMP_SENSOR_DISAGREEMENT` and a suspected channel based on deviation from the consensus/median approach implemented by the firmware quality module.

Three-sensor consistency is not traceable calibration and cannot replace a reference instrument.

## Physical validation plan

Future physical work requires controlled reference measurements, calibration points, uncertainty records, environmental conditions, instrument identifiers, and a completed commissioning report. No physical accuracy, NH3 selectivity, reference traceability, or farm campaign is claimed in this repository.

## Evidence source

Build and test commands are recorded in `docs/11_requirements_traceability.md` and `docs/12_limitations.md`. Detailed historical verification notes remain available in Git history during consolidation.

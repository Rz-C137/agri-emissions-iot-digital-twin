"""Export traceable synthetic calibration coefficients and a holdout report."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from validation.analysis import calibrate, dataset


def apply_calibration(raw, artifact: dict):
    if artifact.get("schema") != "affine-nh3-v1" or artifact.get("units") != "ppm":
        raise ValueError("Unsupported calibration schema or units")
    slope, intercept = artifact["slope"], artifact["intercept"]
    if not np.isfinite([slope, intercept]).all():
        raise ValueError("Nonfinite coefficients")
    return np.asarray(raw, dtype=float) * slope + intercept


def export_report(directory: Path) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    source = dataset()
    fitted, result = calibrate(source)
    artifact = {
        "schema": "affine-nh3-v1",
        "units": "ppm",
        "provenance": "SYNTHETIC",
        "source_sha256": hashlib.sha256(source.to_csv(index=False).encode()).hexdigest(),
        "training_start": str(fitted.timestamp.iloc[0]),
        "training_end": str(fitted.timestamp.iloc[result["train_rows"] - 1]),
        "slope": result["slope"],
        "intercept": result["intercept"],
        "scope": "Default synthetic NH3 model only; not physical sensor coefficients",
    }
    path = directory / "calibration.json"
    path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    holdout = fitted[fitted.split == "Validation"].copy()
    corrected = apply_calibration(holdout.nh3_raw_ppm, loaded)
    error = corrected - holdout.nh3_reference_ppm.to_numpy()
    error = error[np.isfinite(error)]
    bias, spread = float(error.mean()), float(error.std(ddof=1))
    result["agreement"] = {
        "bias_ppm": bias,
        "lower_ppm": bias - 1.96 * spread,
        "upper_ppm": bias + 1.96 * spread,
    }
    (directory / "metrics.json").write_text(
        json.dumps(result, indent=2, allow_nan=False), encoding="utf-8"
    )
    (directory / "report.md").write_text(
        "# Synthetic NH3 validation report\n\n"
        f"Training pairs: {result['fit_pairs']}; chronological holdout rows: {result['validation_rows']}.\n\n"
        f"Raw RMSE: {result['raw']['RMSE_ppm']:.4f} ppm; calibrated RMSE: {result['calibrated']['RMSE_ppm']:.4f} ppm.\n\n"
        f"Descriptive agreement limits: {bias - 1.96 * spread:.4f} to {bias + 1.96 * spread:.4f} ppm; bias {bias:.4f} ppm.\n\n"
        "Limits are mean difference ± 1.96 sample SD, not confidence intervals or physical acceptance limits. Serial correlation, reference uncertainty and concentration-dependent variance limit interpretation.\n\n"
        "Coefficients were reloaded from calibration.json before holdout application. Source SHA-256 and training dates accompany the artifact. No holdout rows train the fit. Raw and calibrated completeness use all holdout rows.\n\n"
        "These synthetic results establish no gas selectivity, traceability, farm performance or emission rate. CH4/N2O in the commissioning bench are interface fixtures, not validated instruments.\n",
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/runs/validation"))
    args = parser.parse_args()
    export_report(args.output)
    print(f"Saved calibration.json, metrics.json and report.md to {args.output}")

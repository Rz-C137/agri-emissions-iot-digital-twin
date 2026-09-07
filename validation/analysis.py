"""Chronological holdout validation of a transparent affine calibration."""

import numpy as np
import pandas as pd

from simulator.engine import Twin


def metrics(reference: np.ndarray, measured: np.ndarray) -> dict[str, float]:
    reference, measured = np.asarray(reference, float), np.asarray(measured, float)
    mask = np.isfinite(reference) & np.isfinite(measured)
    completeness = 100 * mask.mean() if len(mask) else 0.0
    error = measured[mask] - reference[mask]
    total = np.sum((reference[mask] - np.mean(reference[mask])) ** 2) if mask.any() else 0
    return {
        "bias_ppm": float(error.mean()) if len(error) else np.nan,
        "MAE_ppm": float(np.abs(error).mean()) if len(error) else np.nan,
        "RMSE_ppm": float(np.sqrt(np.mean(error**2))) if len(error) else np.nan,
        "R2": float(1 - np.sum(error**2) / total) if total > 0 else np.nan,
        "completeness_pct": completeness,
        "missing_pct": 100 - completeness,
    }


def calibrate(frame: pd.DataFrame, fraction: float = 0.6) -> tuple[pd.DataFrame, dict]:
    """Fit raw signal -> reference on the first block; evaluate on later unseen rows."""
    if not 0 < fraction < 1:
        raise ValueError("Training fraction must lie between zero and one.")
    frame = frame.sort_values("timestamp").reset_index(drop=True).copy()
    cut = int(len(frame) * fraction)
    train = frame.iloc[:cut]
    valid = np.isfinite(train.nh3_raw_ppm) & np.isfinite(train.nh3_reference_ppm)
    valid &= train.quality_flag == "VALID"
    if valid.sum() < 3 or train.loc[valid, "nh3_raw_ppm"].nunique() < 2:
        raise ValueError("Calibration needs at least three valid, varying training pairs.")
    x = train.loc[valid, "nh3_raw_ppm"].to_numpy()
    y = train.loc[valid, "nh3_reference_ppm"].to_numpy()
    slope, intercept = np.linalg.lstsq(np.column_stack([x, np.ones(len(x))]), y, rcond=None)[0]
    frame["nh3_calibrated_ppm"] = slope * frame.nh3_raw_ppm + intercept
    frame["split"] = np.where(frame.index < cut, "Training", "Validation")
    holdout = frame.iloc[cut:]
    return frame, {
        "slope": float(slope),
        "intercept": float(intercept),
        "train_rows": cut,
        "fit_pairs": int(valid.sum()),
        "validation_rows": len(holdout),
        "raw": metrics(holdout.nh3_reference_ppm, holdout.nh3_raw_ppm),
        "calibrated": metrics(holdout.nh3_reference_ppm, holdout.nh3_calibrated_ppm),
    }


def dataset(samples: int = 4320) -> pd.DataFrame:
    twin = Twin()
    twin.step(samples)
    return pd.DataFrame(twin.records)

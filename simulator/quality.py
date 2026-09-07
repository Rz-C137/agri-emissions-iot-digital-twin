"""Attach flags without altering or dropping measurements."""

from dataclasses import dataclass
from datetime import datetime
from math import isfinite

import numpy as np


@dataclass(frozen=True)
class QualityConfig:
    abrupt_ppm: float = 12
    stale_s: float = 120
    outlier_sigma: float = 6
    outlier_enabled: bool = True


def check(
    record: dict, history: list[dict], config: QualityConfig, now: datetime | None = None
) -> str:
    """Evaluate ranges, availability, freshness and a causal robust outlier rule."""
    flags = []
    for key, low, high in [
        ("temperature_c", -20, 60),
        ("relative_humidity_pct", 0, 100),
        ("nh3_raw_ppm", 0, 200),
    ]:
        value = record.get(key)
        if value is None:
            flags.append("MISSING")
        elif not isfinite(value):
            flags.append("INVALID")
        elif not low <= value <= high:
            flags.append("RANGE")
    if record["sensor_status"] != "OK":
        flags.append("COMMUNICATION")
    timestamp = datetime.fromisoformat(record["timestamp"])
    if now and (now - timestamp).total_seconds() > config.stale_s:
        flags.append("STALE")
    value = record.get("nh3_raw_ppm")
    previous = [
        r["nh3_raw_ppm"]
        for r in history[-30:]
        if r.get("nh3_raw_ppm") is not None and isfinite(r["nh3_raw_ppm"])
    ]
    if value is not None and isfinite(value) and previous:
        if abs(value - previous[-1]) > config.abrupt_ppm:
            flags.append("ABRUPT")
        if config.outlier_enabled and len(previous) >= 10:
            median = float(np.median(previous))
            scale = max(0.25, 1.4826 * float(np.median(np.abs(np.array(previous) - median))))
            if abs(value - median) > config.outlier_sigma * scale:
                flags.append("OUTLIER")
    return "|".join(sorted(set(flags))) or "VALID"


# Shared wire contract with firmware/Quality.h. VALID has no bits set.
QUALITY_BITS = {
    "MISSING": 1,
    "RANGE": 2,
    "COMMUNICATION": 4,
    "INVALID": 8,
    "ABRUPT": 16,
    "STALE": 32,
    "OUTLIER": 64,
}


def quality_code(flags: str) -> int:
    """Encode the human-readable pipe-separated quality field without losing information."""
    return sum(QUALITY_BITS[flag] for flag in set(flags.split("|")) if flag != "VALID")

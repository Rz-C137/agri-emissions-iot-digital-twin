"""Temperature sensor agreement logic mirrored from firmware QualityControl."""

from __future__ import annotations

import math
from typing import Any

DEFAULT_THRESHOLD_C = 1.0
TEMP_FAULT_MODES = ("NONE", "DHT_BIAS", "DS18_BIAS", "BMP_BIAS")


def _finite(value: float | None) -> bool:
    return value is not None and math.isfinite(value)


def _median3(a: float, b: float, c: float) -> float:
    values = sorted((a, b, c))
    return values[1]


def assess_temperature_agreement(
    temperature_dht22_c: float | None,
    temperature_ds18b20_c: float | None,
    temperature_bmp180_c: float | None,
    threshold_c: float = DEFAULT_THRESHOLD_C,
) -> dict[str, Any]:
    """Return commissioning status for three temperature channels."""
    readings = {
        "DHT22": temperature_dht22_c,
        "DS18B20": temperature_ds18b20_c,
        "BMP180": temperature_bmp180_c,
    }
    valid = {name: value for name, value in readings.items() if _finite(value)}
    if not valid:
        return {
            "readings": readings,
            "max_disagreement_c": None,
            "threshold_c": threshold_c,
            "status": "MISSING",
            "flag": "MISSING",
            "suspected_sensor": "NONE",
        }

    deltas: list[float] = []
    if _finite(temperature_dht22_c) and _finite(temperature_ds18b20_c):
        deltas.append(abs(temperature_dht22_c - temperature_ds18b20_c))
    if _finite(temperature_dht22_c) and _finite(temperature_bmp180_c):
        deltas.append(abs(temperature_dht22_c - temperature_bmp180_c))
    if _finite(temperature_ds18b20_c) and _finite(temperature_bmp180_c):
        deltas.append(abs(temperature_ds18b20_c - temperature_bmp180_c))
    max_disagreement = max(deltas) if deltas else 0.0

    if max_disagreement <= threshold_c:
        return {
            "readings": readings,
            "max_disagreement_c": max_disagreement,
            "threshold_c": threshold_c,
            "status": "PASS",
            "flag": "VALID",
            "suspected_sensor": "NONE",
        }

    suspected = "NONE"
    if len(valid) == 3:
        ref = _median3(
            temperature_dht22_c,
            temperature_ds18b20_c,
            temperature_bmp180_c,  # type: ignore[arg-type]
        )
        suspected = max(
            valid,
            key=lambda name: abs(valid[name] - ref),
        )
    elif len(valid) == 2:
        names = list(valid)
        mid = sum(valid.values()) / 2.0
        suspected = (
            names[0] if abs(valid[names[0]] - mid) >= abs(valid[names[1]] - mid) else names[1]
        )

    return {
        "readings": readings,
        "max_disagreement_c": max_disagreement,
        "threshold_c": threshold_c,
        "status": "WARNING",
        "flag": "TEMP_SENSOR_DISAGREEMENT",
        "suspected_sensor": suspected,
    }

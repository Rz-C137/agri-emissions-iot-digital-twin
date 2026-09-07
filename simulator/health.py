"""Separate environmental interpretation from operational faults and data quality."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Health:
    environmental_condition: str
    measurement_system: str
    sensor: str
    network: str
    storage: str
    data_quality: str


def assess(record: dict, network: str, storage: str) -> Health:
    """Use raw signal as an indication, never interpret a missing reading as normal air."""
    value = record["nh3_raw_ppm"]
    flags = set(record["quality_flags"].split("|"))
    usable = (
        value is not None
        and isfinite(value)
        and not flags.intersection({"MISSING", "INVALID", "COMMUNICATION", "STALE", "RANGE"})
    )
    condition = "UNKNOWN" if not usable else "ELEVATED" if value > 25 else "BASELINE"
    problems = []
    if record["sensor_status"] != "OK":
        problems.append("SENSOR_FAULT")
    if network != "ONLINE":
        problems.append("COMMUNICATION_INTERRUPTED")
    if storage != "OK":
        problems.append("LOCAL_STORAGE_FAILED")
    return Health(
        condition,
        " | ".join(problems) or "OPERATIONAL",
        record["sensor_status"],
        network,
        storage,
        "VALID" if flags == {"VALID"} else "REVIEW_REQUIRED",
    )

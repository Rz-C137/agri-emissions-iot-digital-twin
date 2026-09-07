"""Environment and instrument models; coefficients are illustrative assumptions."""

from dataclasses import dataclass
from datetime import datetime, timezone

import numpy as np


@dataclass(frozen=True)
class Config:
    seed: int = 42
    interval_s: int = 60
    node_id: str = "virtual-barn-01"
    noise_ppm: float = 0.65
    bias_ppm: float = 2.0
    humidity_coefficient: float = 0.055
    temperature_coefficient: float = 0.09
    drift_ppm_day: float = 0.04
    reference_noise_ppm: float = 0.12
    reference_bias_ppm: float = 0.03
    reference_drift_ppm_day: float = 0.002
    start: datetime = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def __post_init__(self) -> None:
        if self.interval_s <= 0:
            raise ValueError("Sampling interval must be positive.")


class Environment:
    def __init__(self, config: Config):
        self.config = config
        self.rng = np.random.default_rng(config.seed)
        self.transient = 0.0

    def sample(self, index: int, high: bool = False) -> dict[str, float]:
        """Return synthetic covariates, a low-cost signal and a separate reference."""
        c = self.config
        days = index * c.interval_s / 86400
        phase = 2 * np.pi * days
        t = 22 + 4 * np.sin(phase) + self.rng.normal(0, 0.15)
        h = 65 - 12 * np.sin(phase - 0.4) + self.rng.normal(0, 0.5)
        self.transient *= np.exp(-c.interval_s / 900)
        if self.rng.random() < 1 - np.exp(-c.interval_s / 21600):
            self.transient += self.rng.uniform(3, 8)
        truth = 9 + 3 * np.sin(phase - 0.8) + 0.12 * days + self.transient
        truth += 30 if high else 0
        raw = (
            truth
            + c.bias_ppm
            + c.humidity_coefficient * (h - 65)
            + c.temperature_coefficient * (t - 22)
            + c.drift_ppm_day * days
            + self.rng.normal(0, c.noise_ppm)
        )
        reference = (
            truth
            + c.reference_bias_ppm
            + c.reference_drift_ppm_day * days
            + self.rng.normal(0, c.reference_noise_ppm)
        )
        return dict(
            temperature_c=t,
            relative_humidity_pct=h,
            gas_raw=raw * 100,
            nh3_raw_ppm=raw,
            nh3_reference_ppm=reference,
            co2_ppm=800 + 100 * np.sin(phase) + self.rng.normal(0, 8),
        )

"""Acquisition, append-only logging and an explicitly simulated transport."""

import csv
import logging
from dataclasses import asdict, dataclass
from datetime import timedelta
from pathlib import Path

from simulator.model import Config, Environment
from simulator.quality import QualityConfig, check

SCENARIOS = (
    "NORMAL",
    "HIGH_NH3",
    "SENSOR_DISCONNECTED",
    "SENSOR_TIMEOUT",
    "SENSOR_DRIFT",
    "INVALID_READING",
    "NETWORK_OFFLINE",
    "STORAGE_FAILURE",
    "RECOVERY",
)
LOG = logging.getLogger(__name__)


@dataclass
class Event:
    timestamp: str
    severity: str
    event_type: str
    description: str


class Twin:
    def __init__(self, config: Config | None = None, log_path: Path | None = None):
        self.config = config or Config()
        self.environment = Environment(self.config)
        self.quality = QualityConfig(stale_s=2 * self.config.interval_s)
        self.records: list[dict] = []
        self.events: list[dict] = []
        self.pending: dict[int, dict] = {}
        self.delivered: dict[int, dict] = {}
        self.local_pending: dict[int, dict] = {}
        self.local_ids: set[int] = set()
        self.log_path = log_path
        self.scenario = "NORMAL"
        self.scenario_start = 0
        self.network = "ONLINE"
        self.storage = "OK"
        self.retries = 0
        self.outage_start: int | None = None
        self.recovery_time_s: int | None = None

    def event(self, severity: str, kind: str, description: str) -> None:
        timestamp = self.config.start + timedelta(
            seconds=len(self.records) * self.config.interval_s
        )
        self.events.append(asdict(Event(timestamp.isoformat(), severity, kind, description)))
        LOG.info("%s: %s", kind, description)

    def set_scenario(self, scenario: str) -> None:
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        self.scenario = scenario
        self.scenario_start = len(self.records)
        if scenario == "NETWORK_OFFLINE":
            self.network = "OFFLINE"
            if self.outage_start is None:
                self.outage_start = len(self.records)
        elif scenario == "STORAGE_FAILURE":
            self.storage = "FAILED"
        elif scenario == "RECOVERY":
            self.network, self.storage = "ONLINE", "OK"
            self.event(
                "INFO", "RECOVERY", "Recovery requested; pending records await next service cycle."
            )
        self.event(
            "INFO" if scenario in ("NORMAL", "RECOVERY") else "WARNING",
            scenario,
            f"Scenario changed to {scenario}.",
        )

    def _persist(self, record: dict) -> bool:
        if self.storage != "OK":
            return False
        if self.log_path:
            try:
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
                header = not self.log_path.exists() or self.log_path.stat().st_size == 0
                with self.log_path.open("a", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(record))
                    if header:
                        writer.writeheader()
                    writer.writerow(record)
            except OSError as exc:
                self.storage = "FAILED"
                self.event("ERROR", "STORAGE_FAILURE", f"Local write failed: {exc}")
                return False
        self.local_ids.add(record["sequence"])
        return True

    def step(self, count: int = 1) -> dict:
        """Advance simulated time; preserve all attempts and retry pending deliveries."""
        if count < 1:
            raise ValueError("Step count must be positive.")
        for _ in range(count):
            index = len(self.records)
            values = self.environment.sample(index, self.scenario == "HIGH_NH3")
            sensor = "OK"
            if self.scenario in ("SENSOR_DISCONNECTED", "SENSOR_TIMEOUT"):
                sensor = "DISCONNECTED" if self.scenario == "SENSOR_DISCONNECTED" else "TIMEOUT"
                for key in ("nh3_raw_ppm", "gas_raw"):
                    values[key] = None
                self.retries += 1
                self.event(
                    "ERROR",
                    "SENSOR_RETRY",
                    f"Gas acquisition failed ({sensor}); retry next sample.",
                )
            elif self.scenario == "INVALID_READING":
                values["nh3_raw_ppm"] = float("nan")
            elif self.scenario == "SENSOR_DRIFT":
                values["nh3_raw_ppm"] += (index - self.scenario_start + 1) * 0.3
            record = dict(
                timestamp=(
                    self.config.start + timedelta(seconds=index * self.config.interval_s)
                ).isoformat(),
                node_id=self.config.node_id,
                sequence=index,
                **values,
                nh3_calibrated_ppm=None,
                sensor_status=sensor,
                network_status=self.network,
                storage_status=self.storage,
                quality_flag="",
                buffered=self.network != "ONLINE",
                scenario=self.scenario,
                simulated=True,
            )
            record["quality_flag"] = check(record, self.records, self.quality)
            if not self._persist(record):
                record["storage_status"] = "FAILED"
                self.local_pending[index] = record.copy()
            self.pending[index] = record.copy()
            if self.network == "ONLINE":
                backlog = sum(r["buffered"] for r in self.pending.values())
                self.delivered.update(self.pending)
                self.pending.clear()
                if self.outage_start is not None:
                    self.recovery_time_s = (index - self.outage_start) * self.config.interval_s
                    self.event(
                        "INFO",
                        "SYNCHRONIZED",
                        f"Simulated receiver acknowledged {backlog} buffered records; no gaps.",
                    )
                    self.outage_start = None
            if self.storage == "OK" and self.local_pending:
                for key, pending in list(self.local_pending.items()):
                    if not self._persist(pending):
                        break
                    del self.local_pending[key]
                if not self.local_pending:
                    self.event("INFO", "STORAGE_RECOVERED", "Pending local records written.")
            self.records.append(record)
        return self.records[-1]

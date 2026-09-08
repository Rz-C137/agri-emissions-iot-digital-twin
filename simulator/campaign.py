"""Reproducible multi-gas commissioning with a durable local outbox and mock receiver."""

import argparse
import json
import math
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from simulator.modbus import REQUEST_BODY, decode_reference, frame, reference_reply


class Store:
    """SQLite commits model a durable node spool, NOT ESP32 flash or SD performance."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, payload TEXT NOT NULL, ack INTEGER NOT NULL DEFAULT 0)"
        )
        self.db.commit()

    def put(self, record: dict) -> None:
        payload = json.dumps(record, sort_keys=True, allow_nan=False)
        with self.db:
            old = self.db.execute(
                "SELECT payload FROM records WHERE id=?", (record["id"],)
            ).fetchone()
            if old and old[0] != payload:
                raise ValueError("Identity collision with different payload")
            self.db.execute(
                "INSERT OR IGNORE INTO records(id,payload) VALUES (?,?)", (record["id"], payload)
            )

    def rows(self, pending: bool = False) -> list[dict]:
        query = "SELECT payload FROM records" + (" WHERE ack=0" if pending else "") + " ORDER BY id"
        return [json.loads(row[0]) for row in self.db.execute(query)]

    def drain(self, receiver, interrupt_after_receive: bool = False) -> None:
        for record in self.rows(pending=True):
            receiver.put(record)  # Commit receiver before acknowledging locally.
            if interrupt_after_receive:
                raise ConnectionError("Injected disconnect after receiver commit, before ack")
            with self.db:
                self.db.execute("UPDATE records SET ack=1 WHERE id=?", (record["id"],))

    def close(self):
        self.db.close()


def acquire(
    sequence: int, run_id: str = "campaign-v1", fault: str = "OK", site: str = "barn"
) -> dict:
    if site not in ("barn", "manure") or sequence < 0:
        raise ValueError("Invalid campaign site or sequence")
    phase = sequence * 2 * math.pi / 60
    multiplier = 1.0 if site == "barn" else 1.5
    values = tuple(
        multiplier * v
        for v in (
            12 + 4 * math.sin(phase),
            8 + 3 * math.sin(phase + 0.5),
            0.6 + 0.2 * math.sin(phase + 1),
        )
    )
    response = reference_reply(frame(REQUEST_BODY), values, fault)
    status = "VALID"
    try:
        reference = decode_reference(response)
    except (ValueError, TimeoutError) as error:
        reference = dict.fromkeys(("nh3", "ch4", "n2o"))
        status = str(error)
    record = {
        "id": f"{run_id}/node01/{sequence:06d}",
        "run_id": run_id,
        "node_id": "node01",
        "sequence": sequence,
        "site": site,
        "timestamp": (
            datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=sequence)
        ).isoformat(),
        "provenance": "SYNTHETIC",
        "reference_status": status,
        "request_hex": frame(REQUEST_BODY).hex(" "),
        "response_hex": response.hex(" "),
        "temperature_c": 22 + 3 * math.sin(phase),
        "humidity_pct": 65 - 10 * math.sin(phase),
    }
    for gas, truth, bias in zip(("nh3", "ch4", "n2o"), values, (2, 0.8, 0.08)):
        record[f"{gas}_raw_ppm"] = round(truth + bias + 0.1 * bias * math.sin(sequence * 1.7), 4)
        record[f"{gas}_reference_ppm"] = reference[gas]
    return record


def run_campaign(directory: Path, samples: int = 120, site: str = "barn") -> dict:
    """Repeatable replay: timeout 30..34, CRC 60..64, network outage 20..79."""
    if samples < 1:
        raise ValueError("samples must be positive")
    node, receiver = Store(directory / "node.sqlite"), Store(directory / "receiver.sqlite")
    try:
        for sequence in range(samples):
            fault = "TIMEOUT" if 30 <= sequence < 35 else "BAD_CRC" if 60 <= sequence < 65 else "OK"
            node.put(acquire(sequence, run_id=f"commissioning-v1-{site}", fault=fault, site=site))
            if not 20 <= sequence < 80:
                node.drain(receiver)
        node.drain(receiver)
        records = receiver.rows()
        summary = {
            "scope": "Synthetic protocol and persistence test; no physical gas measurements",
            "stored_records": len(records),
            "pending_records": len(node.rows(pending=True)),
            "valid_reference_records": sum(r["reference_status"] == "VALID" for r in records),
            "reference_fault_records": sum(r["reference_status"] != "VALID" for r in records),
        }
        (directory / "campaign.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
        (directory / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return summary
    finally:
        node.close()
        receiver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/runs/commissioning"))
    parser.add_argument("--site", choices=["barn", "manure"], default="barn")
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.output, site=args.site), indent=2))

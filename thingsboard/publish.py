"""Opt-in TLS MQTT publisher with QoS 1 and acknowledged checkpointing."""

import argparse
import json
import logging
import os
from pathlib import Path

import paho.mqtt.client as mqtt
import pandas as pd


def payload_for(record: dict) -> str:
    """Serialize a UTC record; omit nonfinite scalars while retaining quality provenance."""
    # pandas normalizes NaN to null; the final strict JSON encoder rejects regressions.
    row = json.loads(pd.Series(record).to_json())
    timestamp = pd.Timestamp(row.pop("timestamp"))
    if pd.isna(timestamp) or timestamp.tzinfo is None:
        raise ValueError("Telemetry requires an available timezone-aware UTC timestamp.")
    values = {key: value for key, value in row.items() if value is not None}
    values["simulated"] = True
    return json.dumps({"ts": int(timestamp.timestamp() * 1000), "values": values}, allow_nan=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument(
        "--checkpoint", type=Path, default=Path("data/runs/publisher-checkpoint.json")
    )
    args = parser.parse_args()
    host, token = os.getenv("THINGSBOARD_HOST"), os.getenv("THINGSBOARD_TOKEN")
    if not host or not token:
        parser.error("Export THINGSBOARD_HOST and THINGSBOARD_TOKEN before publishing.")
    frame = pd.read_csv(args.csv)
    identity = str(args.csv.resolve()) + ":" + str(args.csv.stat().st_mtime_ns)
    saved = json.loads(args.checkpoint.read_text()) if args.checkpoint.exists() else {}
    start = saved.get("next_row", 0) if saved.get("source") == identity else 0
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(token)
    client.tls_set()
    client.connect(host, int(os.getenv("THINGSBOARD_PORT", "8883")), 60)
    client.loop_start()
    try:
        for index in range(start, len(frame)):
            payload = payload_for(frame.iloc[index].to_dict())
            info = client.publish("v1/devices/me/telemetry", payload, qos=1)
            info.wait_for_publish(timeout=10)
            if not info.is_published():
                raise TimeoutError(
                    "Broker acknowledgement missing; rerun to retry from checkpoint."
                )
            args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.checkpoint.with_suffix(".tmp")
            temporary.write_text(json.dumps({"source": identity, "next_row": index + 1}))
            temporary.replace(args.checkpoint)
    finally:
        client.disconnect()
        client.loop_stop()
    logging.basicConfig(level=logging.INFO)
    logging.info("Synthetic telemetry acknowledged through row %s", len(frame))


if __name__ == "__main__":
    main()

"""Generate a deterministic dataset and holdout metrics without the dashboard."""

import argparse
import json
import logging
from pathlib import Path

from validation.analysis import calibrate, dataset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=4320)
    parser.add_argument("--output", type=Path, default=Path("data/demo.csv"))
    args = parser.parse_args()
    frame, report = calibrate(dataset(args.samples))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)
    args.output.with_suffix(".metrics.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    logging.basicConfig(level=logging.INFO)
    logging.info("Wrote %s explicitly simulated records to %s", len(frame), args.output)


if __name__ == "__main__":
    main()

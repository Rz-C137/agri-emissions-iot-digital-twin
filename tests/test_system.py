from datetime import timedelta

import numpy as np
import pandas as pd
import pytest

from simulator.engine import Twin
from simulator.quality import QualityConfig, check
from validation.analysis import calibrate, metrics


def test_reproducibility():
    a, b = Twin(), Twin()
    a.step(100)
    b.step(100)
    assert a.records == b.records


@pytest.mark.parametrize(
    "scenario,status", [("SENSOR_DISCONNECTED", "DISCONNECTED"), ("SENSOR_TIMEOUT", "TIMEOUT")]
)
def test_sensor_fault_and_recovery(scenario, status):
    twin = Twin()
    twin.set_sensor(scenario)
    r = twin.step()
    assert r["nh3_raw_ppm"] is None and r["gas_channel_status"] == status
    assert "COMMUNICATION" in r["quality_flags"] and twin.retries == 1
    assert r["temperature_c"] is not None
    twin.restore_all()
    assert twin.step()["sensor_status"] == "OK"


def test_network_no_silent_loss(tmp_path):
    twin = Twin(log_path=tmp_path / "records.csv")
    twin.step(4)
    twin.set_network(False)
    twin.step(40)
    assert len(twin.pending) == 40 and len(twin.local_ids) == 44
    assert len(pd.read_csv(twin.log_path)) == 44
    twin.restore_all()
    twin.step()
    assert not twin.pending
    assert set(twin.delivered) == set(range(45))
    assert twin.recovery_time_s == 2400
    assert twin.records[4]["buffered"] is True
    recovery_event = next(e for e in twin.events if e["event_type"] == "SYNCHRONIZED")
    assert recovery_event["timestamp"] == twin.records[-1]["timestamp"]


def test_combined_outage_and_storage_recovery(tmp_path):
    twin = Twin(log_path=tmp_path / "data.csv")
    twin.set_network(False)
    twin.set_storage(False)
    twin.step(10)
    assert len(twin.local_pending) == len(twin.pending) == 10
    twin.restore_all()
    twin.step()
    assert not twin.local_pending and not twin.pending
    assert set(twin.delivered) == twin.local_ids == set(range(11))
    assert len(pd.read_csv(twin.log_path)) == 11


def test_actual_write_failure_is_visible(tmp_path):
    twin = Twin(log_path=tmp_path)
    assert twin.step()["storage_status"] == "FAILED"
    assert len(twin.local_pending) == 1


def test_quality_preserves_invalid_and_detects_stale_range_abrupt():
    twin = Twin()
    twin.step(20)
    twin.set_sensor("INVALID_READING")
    record = twin.step()
    assert np.isnan(record["nh3_raw_ppm"]) and "INVALID" in record["quality_flags"]
    record = dict(twin.records[0], relative_humidity_pct=120, nh3_raw_ppm=100)
    flags = check(
        record, twin.records[:20], QualityConfig(), twin.config.start + timedelta(seconds=300)
    )
    assert all(flag in flags for flag in ["RANGE", "ABRUPT", "STALE", "OUTLIER"])


def test_metrics_known_errors_and_undefined_r2():
    report = metrics(np.array([1, 2, 3, 4]), np.array([2, 3, 4, np.nan]))
    assert report["bias_ppm"] == report["MAE_ppm"] == report["RMSE_ppm"] == 1
    assert report["completeness_pct"] == 75
    assert report["R2"] == -0.5
    assert np.isnan(metrics(np.array([1, 1]), np.array([1, 1]))["R2"])


def test_calibration_does_not_learn_from_holdout():
    twin = Twin()
    twin.step(200)
    frame = pd.DataFrame(twin.records)
    _, first = calibrate(frame)
    frame.loc[120:, "nh3_reference_ppm"] += 100
    _, second = calibrate(frame)
    assert first["slope"] == second["slope"]
    assert first["intercept"] == second["intercept"]
    assert second["calibrated"]["RMSE_ppm"] > 90


@pytest.mark.parametrize("first", ["network", "storage"])
def test_independent_recovery_and_record_accounting(tmp_path, first):
    twin = Twin(log_path=tmp_path / "records.csv")
    twin.set_sensor("SENSOR_DISCONNECTED")
    twin.set_network(False)
    twin.set_storage(False)
    twin.step(8)
    if first == "network":
        twin.set_network(True)
    else:
        twin.set_storage(True)
    twin.step(3)
    assert twin.sensor_mode == "SENSOR_DISCONNECTED"
    assert twin.storage == ("FAILED" if first == "network" else "OK")
    assert twin.network == ("ONLINE" if first == "network" else "OFFLINE")
    assert len(twin.pending) == (0 if first == "network" else 11)
    assert len(twin.local_pending) == (11 if first == "network" else 0)
    twin.set_sensor("NORMAL")
    twin.step()
    assert twin.records[-1]["gas_channel_status"] == "OK"
    twin.restore_all()
    twin.step()
    assert set(twin.delivered) == twin.local_ids == set(range(13))
    disk = pd.read_csv(twin.log_path)
    assert disk.sequence.is_unique and set(disk.sequence) == set(range(13))


def test_repeated_state_requests_do_not_restart_faults():
    twin = Twin()
    twin.set_sensor("SENSOR_DRIFT")
    twin.step(4)
    twin.set_sensor("SENSOR_DRIFT")
    assert twin.sensor_start == 0
    assert len([e for e in twin.events if e["event_type"] == "SENSOR_STATE"]) == 1
    twin.set_network(False)
    twin.step(4)
    twin.set_network(False)
    assert twin.outage_start == 4


def test_environment_health_is_separate_from_system_and_quality():
    from simulator.health import assess

    twin = Twin()
    twin.step(20)
    twin.set_environment("HIGH_NH3")
    row = twin.step()
    health = assess(row, twin.network, twin.storage)
    assert health.environmental_condition == "ELEVATED"
    assert health.measurement_system == "OPERATIONAL"
    assert health.data_quality == "REVIEW_REQUIRED"
    twin.set_network(False)
    twin.set_sensor("SENSOR_TIMEOUT")
    row = twin.step()
    assert assess(row, twin.network, twin.storage).environmental_condition == "UNKNOWN"
    twin.restore_all()
    assert twin.environment_mode == "HIGH_NH3"


def test_quality_contract_and_duplicate_guard():
    from simulator.quality import quality_code

    assert quality_code("MISSING|COMMUNICATION") == 5
    assert quality_code("VALID") == 0
    twin = Twin()
    twin.step()
    twin.delivered[1] = twin.records[0]
    with pytest.raises(RuntimeError, match="Duplicate sequence"):
        twin.step()

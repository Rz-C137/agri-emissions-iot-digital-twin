import json

import pytest

from simulator.engine import Twin
from thingsboard.publish import payload_for


def test_invalid_telemetry_is_strict_json_with_quality_provenance():
    twin = Twin()
    twin.set_sensor("INVALID_READING")
    payload = json.loads(payload_for(twin.step()))
    assert "nh3_raw_ppm" not in payload["values"]
    assert payload["values"]["quality_code"] == 8
    assert payload["values"]["quality_flags"] == "INVALID"
    assert payload["ts"] == 1767225600000


def test_unsynchronized_time_is_not_published_as_now():
    record = Twin().step()
    record["timestamp"] = None
    with pytest.raises(ValueError, match="timestamp"):
        payload_for(record)

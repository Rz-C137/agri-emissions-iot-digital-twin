import pytest

from simulator.campaign import Store, acquire, run_campaign
from simulator.modbus import REQUEST_BODY, checked, crc16, decode_reference, frame, reference_reply


def test_modbus_known_crc_and_wire_contract():
    assert crc16(b"123456789") == 0x4B37
    assert frame(bytes.fromhex("01 03 00 00 00 0a")).hex() == "01030000000ac5cd"
    packet = reference_reply(frame(REQUEST_BODY), (12.34, 5.67, 0.891))
    assert packet[3:9] == bytes.fromhex("04 d2 02 37 03 7b")
    assert decode_reference(packet) == {"nh3": 12.34, "ch4": 5.67, "n2o": 0.891}
    with pytest.raises(ValueError):
        decode_reference(packet[:-1] + bytes([packet[-1] ^ 1]))
    with pytest.raises(ValueError):
        decode_reference(frame(bytes([2]) + checked(packet)[1:]))
    with pytest.raises(TimeoutError):
        decode_reference(b"")


def test_reference_fault_preserves_raw_without_stale_reference():
    for fault in ("TIMEOUT", "BAD_CRC"):
        row = acquire(30, fault=fault)
        assert row["nh3_raw_ppm"] > 0
        assert row["nh3_reference_ppm"] is None
        assert row["reference_status"] != "VALID"


def test_committed_outbox_reopen_and_lost_ack_are_idempotent(tmp_path):
    node = Store(tmp_path / "node.sqlite")
    receiver = Store(tmp_path / "receiver.sqlite")
    node.put(acquire(0))
    with pytest.raises(ConnectionError):
        node.drain(receiver, interrupt_after_receive=True)
    node.close()
    node = Store(tmp_path / "node.sqlite")
    assert len(node.rows(pending=True)) == 1
    node.drain(receiver)
    assert len(receiver.rows()) == 1 and not node.rows(pending=True)
    changed = acquire(0)
    changed["nh3_raw_ppm"] += 1
    with pytest.raises(ValueError, match="collision"):
        node.put(changed)
    node.close()
    receiver.close()


def test_campaign_rerun_has_no_duplicate_records(tmp_path):
    first = run_campaign(tmp_path)
    assert first["stored_records"] == 120
    assert first["reference_fault_records"] == 10
    assert first["pending_records"] == 0
    assert run_campaign(tmp_path) == first


def test_calibration_export_reload_and_metadata(tmp_path):
    import json

    import numpy as np

    from validation.report import apply_calibration, export_report

    result = export_report(tmp_path)
    artifact = json.loads((tmp_path / "calibration.json").read_text())
    assert len(artifact["source_sha256"]) == 64
    assert result["calibrated"]["RMSE_ppm"] < result["raw"]["RMSE_ppm"]
    assert np.isnan(apply_calibration([np.nan], artifact)[0])
    with pytest.raises(ValueError):
        apply_calibration([1], {**artifact, "units": "ppb"})

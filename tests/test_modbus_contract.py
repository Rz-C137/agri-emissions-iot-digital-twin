"""Run identical vectors through Python and the hardware-independent C++ client."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from simulator.modbus import REQUEST_BODY, decode_reference, frame, reference_reply

ROOT = Path(__file__).resolve().parents[1]
REQUEST_HEX = "01030000000305cb"
# Deliberately fixed bytes rather than deriving the expected response with the code under test.
RESPONSE_BODY = bytes.fromhex("01030604d20237037b")


def test_python_contract():
    values = (12.34, 5.67, 0.891)
    assert frame(REQUEST_BODY).hex() == REQUEST_HEX
    assert reference_reply(bytes.fromhex(REQUEST_HEX), values) == frame(RESPONSE_BODY)
    assert decode_reference(frame(RESPONSE_BODY)) == dict(zip(("nh3", "ch4", "n2o"), values))


def test_native_modbus_contract(tmp_path):
    compiler = shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        assert not os.environ.get("CI"), "Native C++ compiler required in CI"
        pytest.skip("Native compiler unavailable locally; required on Linux CI")
    binary = tmp_path / "modbus-test.exe"
    subprocess.run(
        [
            compiler,
            "-std=c++11",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-I" + str(ROOT / "firmware/include"),
            str(ROOT / "firmware/src/ModbusRtu.cpp"),
            str(ROOT / "firmware/test/modbus_native.cpp"),
            "-o",
            str(binary),
        ],
        check=True,
    )
    subprocess.run(
        [str(binary), REQUEST_HEX, frame(RESPONSE_BODY).hex(), "12.34", "5.67", "0.891"], check=True
    )

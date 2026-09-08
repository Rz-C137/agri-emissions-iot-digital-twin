"""Byte-level Modbus RTU reference emulator; no serial port or RS-485 electrical model."""

import math
import struct

GASES = ("nh3", "ch4", "n2o")
SCALES = (100, 100, 1000)
REQUEST_BODY = bytes.fromhex("01 03 00 00 00 03")


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0xA001 if crc & 1 else 0)
    return crc


def frame(body: bytes) -> bytes:
    return body + struct.pack("<H", crc16(body))


def checked(packet: bytes) -> bytes:
    if len(packet) < 4 or crc16(packet[:-2]) != int.from_bytes(packet[-2:], "little"):
        raise ValueError("CRC_OR_LENGTH_ERROR")
    return packet[:-2]


def reference_reply(request: bytes, concentrations: tuple, fault: str = "OK") -> bytes:
    """One virtual unit, FC03, three unsigned holding registers at offset zero."""
    if fault not in ("OK", "TIMEOUT", "BAD_CRC"):
        raise ValueError("Unknown reference fault")
    if fault == "TIMEOUT":
        return b""
    body = checked(request)
    if body != REQUEST_BODY:
        raise ValueError("Unsupported request in this intentionally narrow emulator")
    if len(concentrations) != 3:
        raise ValueError("Expected NH3, CH4, N2O")
    words = []
    for value, scale in zip(concentrations, SCALES):
        if not math.isfinite(value) or not 0 <= value * scale <= 65535:
            raise ValueError("Reference register outside representable range")
        words.append(round(value * scale))
    packet = frame(bytes([1, 3, 6]) + struct.pack(">3H", *words))
    return packet[:-1] + bytes([packet[-1] ^ 1]) if fault == "BAD_CRC" else packet


def decode_reference(packet: bytes) -> dict:
    if not packet:
        raise TimeoutError("REFERENCE_TIMEOUT")
    body = checked(packet)
    if len(body) != 9 or body[:3] != bytes([1, 3, 6]):
        raise ValueError("UNEXPECTED_UNIT_FUNCTION_OR_LENGTH")
    return dict(zip(GASES, (n / s for n, s in zip(struct.unpack(">3H", body[3:]), SCALES))))

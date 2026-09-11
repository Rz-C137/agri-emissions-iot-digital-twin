# Shared Modbus RTU contract and optional firmware client

The Python commissioning emulator and the ESP32 firmware implement the same narrow reference-device contract. C++ protocol logic has no Arduino dependency and is exercised with a fake transport on the host. The UART2 adapter is separately compiled. No physical RS-485 electrical bus, transceiver or timing measurement has been tested.

| Contract | Python | C++ firmware |
| --- | --- | --- |
| Unit / function | 1 / 03 | 1 / 03 |
| Holding register start / count | zero-based 0 / 3 | zero-based 0 / 3 |
| Register 0 | NH3, uint16 / 100 ppm | same |
| Register 1 | CH4, uint16 / 100 ppm | same |
| Register 2 | N2O, uint16 / 1000 ppm | same |
| Word bytes | high byte first | same |
| CRC | initial 0xFFFF, reflected polynomial 0xA001, low byte first on wire | same |
| Request | `01 03 00 00 00 03 05 cb` | same |
| Successful reply | 11 bytes, including unit/function/byte count 6 and CRC | same |

`simulator/modbus.py` and `firmware/include/ModbusRtu.h` / `firmware/src/ModbusRtu.cpp` are the two language implementations. `tests/test_modbus_contract.py` locks their shared request bytes and the register vector 1234/567/891 (12.34/5.67/0.891 ppm), compiles the native C++ runner and supplies the same response to it. This intentional duplication across languages is documented and tested; the Wokwi copies are generated with `python wokwi/export.py`, not independently maintained.

The client creates requests, validates complete reply length, CRC, unit, function and byte count, then extracts and scales registers. Errors return `TIMEOUT`, `LENGTH_ERROR`, `CRC_ERROR`, `UNIT_ERROR`, `FUNCTION_ERROR` or `TRANSPORT_ERROR`. Every failed result starts with NaN gas values, so a previous reading cannot silently become current. Python and C++ reject the same malformed contract; their diagnostic categories/validation order are not identical. Modbus exception responses are rejected as unsupported; there is no full exception decoding, arbitrary register access or multi-device master.

## Firmware use

The normal `esp32dev` environment and Wokwi sketch keep `AGRI_ENABLE_RS485=0`. UART2 and GPIO27 are not initialized or polled in that path. Existing sensor acquisition, CSV and MQTT behavior remain unchanged.

Compile the optional path with:

```bash
python -m platformio run -d firmware -e esp32dev_rs485
```

This environment defines `AGRI_ENABLE_RS485=1`. No upload is performed by that command. `setup()` initializes the adapter; after each normal acquisition, the loop polls the reference and prints a separate `# MODBUS_REFERENCE,sequence=...,status=...` serial record. Only valid replies include gas values. These reference diagnostics are not added to the existing CSV/MQTT measurement schema, and are not connected to the Python dashboard. The existing surrogate NH3 fields remain missing.

`Rs485Transport` implements the portable `ModbusRtu::Transport` interface. It uses UART2 TX17/RX16 and GPIO27 for tied DE/active-low RE, with a MAX3485-class external 3.3 V transceiver. These pins do not overlap DHT4, ADC34, LED2 or SD18/19/23/5 on the configured `esp32dev` target. Check the exact physical module: some PSRAM variants reserve 16/17. The [wiring plan](marvela_alignment.md#pin-plan-implemented-node-and-proposed-industrial-extension) remains a proposed bench setup.

Configuration: baud and response timeout are in `Config.h` (9600 and 250 ms). `begin(baud, parity)` accepts 1200–115200 baud and `SERIAL_8E1`, `SERIAL_8O1` or `SERIAL_8N2`; the call in `main.cpp` selects 8E1. All use 11-bit characters. GPIO27 LOW receives; HIGH transmits. `Serial2.flush(true)` waits for TX completion before returning LOW; this behavior was checked against the installed Arduino ESP32 2.0.17 core, not measured on a wire. See [Espressif's serial API](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/serial.html).

The adapter discards stale input until a quiet interval, bounded by the configured timeout. It waits for a reply-ending quiet interval of 3.5 characters (1.75 ms above 19200 baud), rejects overflow and never accepts a truncated prefix of an oversized frame. No bytes means timeout; a partial reply is a length error. The poll is synchronous: preflight quiet wait and response wait can each consume 250 ms, plus UART transmission. It does not establish hard real-time deadlines, per-byte 1.5-character timing enforcement, collision handling or immunity to late responses from an earlier request. RTU has no transaction ID; those physical/integration cases need bench validation.

## Verification and interview use

`python -m pytest -q` runs Python checks and, when a native compiler is available, compiles/runs `firmware/test/modbus_native.cpp` with warnings treated as errors. Linux CI requires the compiler and runs the existing native quality test too. Native cases include the known CRC `123456789 → 0x4B37`, exact request, valid response/scaling, corrupted CRC, wrong unit/function/byte count, every nonempty truncated length, oversized reply, timeout and mock transport failure.

Show the existing dashboard's CRC/timeout and recovery controls during the interview, then point to this contract and successful CI. Use the already-generated validation report. The accurate claim is: **I implemented and host-tested the Modbus RTU protocol logic in ESP32 firmware; the physical RS-485 electrical layer remains a proposed bench test.**

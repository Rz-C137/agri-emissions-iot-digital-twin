# Wokwi Source Package

The user-facing Wokwi procedure is maintained in the repository [README](../README.md#Wokwi-workflow). This directory is the authoritative virtual embedded source package:

- `diagram.json` is the virtual wiring source of truth.
- `sketch.ino` and the copied modular files are browser-compatible exports.
- `libraries.txt` declares browser dependencies.
- `flasher_args.json`, `wokwi.toml`, and prepared binaries support custom-firmware loading.
- `export.py` refreshes browser-compatible source files from `firmware/`.

Wokwi demonstrates pin-exact embedded integration and firmware behaviour. It does not establish physical voltage safety, soldering, RS-485 electrical performance, NH3 selectivity, sensor accuracy, or farm deployment. MQ-2 remains an analog acquisition surrogate only.

Prepare the compiled artifact with:

```powershell
python -m platformio run -d firmware -e esp32dev
python tools/prepare_wokwi_firmware.py
```

Runtime and serial output are evidence only when an actual Wokwi session is observed and recorded.

# Free Wokwi browser reproduction

This workflow uses the Community browser editor, not Wokwi for VS Code, CI tokens, a private gateway or binary-file upload. The local Python demonstration remains the reliable interview route.

1. Open [a new ESP32 browser project](https://wokwi.com/projects/new/esp32). Sign in if needed to save a public copy.
2. Replace the editor's `diagram.json` contents with this directory's `diagram.json`.
3. Replace `sketch.ino` with the provided file. It is the firmware scheduler adapted only by filename for Arduino's browser build.
4. Use the editor tab menu to create the following files, copying the identically named files generated in this directory: `Config.h`, `Measurement.h`, `Quality.h`, `SystemState.h`, `Sensors.h`, `Sensors.cpp`, `Logger.h`, `Logger.cpp`, `FaultManager.h`, `Telemetry.h`, `Telemetry.cpp`.
5. Copy `libraries.txt`, or use Library Manager to add **DHT sensor library**, **Adafruit Unified Sensor** and **PubSubClient**. The generated libraries file requests the same versions as PlatformIO.
6. Press the green Start button. Open the serial monitor at 115200. Wait at least five simulated seconds for a measurement row. NTP is optional; unsynchronized epoch is zero and uptime remains available.
7. Click DHT22 to change temperature/humidity and click MQ2 to change its gas-slider setting. Observe the raw ADC signal; no NH₃ conversion is performed. Stop and remove the DHT signal connection, then restart to observe communication errors and retries.
8. For network loss/recovery in a controlled repeatable interview, use the Python dashboard. Browser MQTT requires a publicly reachable test broker with permitted access; default firmware leaves it disabled. The Community gateway cannot expose an arbitrary localhost broker.

The microSD component provides a simulated filesystem for runtime logging. No paid custom binary upload is needed. Inspect logging state via serial; persistence/export across stopped simulations is not assumed. Browser UI controls may change; the official [ESP32 guide](https://docs.wokwi.com/guides/esp32), [diagram schema](https://docs.wokwi.com/diagram-format) and [microSD reference](https://docs.wokwi.com/parts/wokwi-microsd-card) explain the supported primitives.

## Analog wiring caveat

The MQ2 diagram is simulation-only: VCC goes to 5 V and AO to ADC GPIO 34. This direct analog connection must not be copied blindly to physical hardware. A real module's output may exceed ESP32 input limits; characterize it and implement suitable signal conditioning before connection. The [MQ2 simulator reference](https://docs.wokwi.com/parts/wokwi-gas-sensor) describes a multi-gas component, not selective NH₃ measurement.

## Refresh browser files after firmware edits

From the repository root, run `python wokwi/export.py`. It copies the modular source files; do not maintain divergent firmware implementations. Then repeat the corresponding browser copy steps. No paid integration is required. Actual browser execution is an external verification step, distinct from the completed PlatformIO build.

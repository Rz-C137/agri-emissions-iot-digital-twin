# ESP32 acquisition demonstrator

Install free PlatformIO Core (`python -m pip install platformio`) and run from this directory:

```bash
python -m platformio run
```

The build targets `esp32dev` using Arduino on Espressif32 6.10.0. DHT22 uses GPIO 4, analog gas uses ADC1 GPIO 34 (avoiding ADC2/WiFi contention), microSD uses SPI SCK 18, MISO 19, MOSI 23 and CS 5. GPIO 2 is a status LED. Serial baud is 115200.

## Configuration

The default Wokwi guest WiFi credentials are public simulator settings, not secrets. MQTT_HOST is empty, so no unsolicited broker transmission occurs. To use a trusted local test broker, create ignored `include/secrets.h`:

```cpp
#pragma once
#define WIFI_SSID "your-test-network"
#define WIFI_PASSWORD "your-test-password"
#define MQTT_HOST "your-local-broker-host"
#define MQTT_PORT 1883
```

This firmware's unauthenticated non-TLS MQTT is intended only for an isolated trusted demonstration network with synthetic data. Use the separate TLS Python publisher for ThingsBoard; do not place a cloud token into a public Wokwi project. No secrets file is distributed.

## Behavior and limits

- Acquires every five seconds independently of whether the MQTT client is connected.
- DHT communication failures produce NaN/quality bits and a next-sample retry event.
- CSV logging to microSD and serial preserves raw temperature, humidity and ADC counts. NH₃ columns are empty.
- Uses NTP epoch seconds when available and monotonic 64-bit uptime otherwise; zero epoch means unsynchronized.
- Retries WiFi/MQTT and SD mounting every ten seconds. MQTT connection attempts can block briefly; this is not a hard real-time scheduler.
- Buffers up to 120 records in RAM. On overflow, it counts and reports each rejected telemetry record. Healthy SD logging continues.
- Drains records after client reconnect. QoS 0 publish success is not broker acknowledgement. SD records are not automatically replayed, and failed local writes are not backfilled.
- The emitted `simulated=true` and WOKWI_SURROGATE scenario are intended for this virtual demonstration. Physical deployment would need explicit provenance changes plus validation, not just a board upload.

The portable `Quality.h` function has an assertion-based native test. If a C++ compiler is installed:

```bash
g++ -std=c++11 -Iinclude test/quality_native.cpp -o quality-test
./quality-test
```

The Python fault engine is richer than the firmware. No automatic browser fault injection, real MQ2 disconnection detection, reboot persistence or laboratory testing is claimed.

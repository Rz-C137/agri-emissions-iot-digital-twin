#include "Sensors.h"
#include <Arduino.h>
#include <esp_timer.h>
#include <time.h>

void Sensors::begin() { dht.begin(); analogReadResolution(12); }
Measurement Sensors::acquire(uint32_t sequence) {
    Measurement m;
    m.sequence = sequence;
    m.uptime_ms = esp_timer_get_time() / 1000;
    const auto now = time(nullptr);
    m.epoch_s = now > 1700000000 ? now : 0;
    m.temperature_c = dht.readTemperature();
    m.relative_humidity_pct = dht.readHumidity();
    m.gas_raw = analogRead(Config::GAS_PIN);
    m.sensor_ok = std::isfinite(m.temperature_c) && std::isfinite(m.relative_humidity_pct);
    // An analog voltage alone cannot establish gas identity or detect every disconnected wire.
    return m;
}

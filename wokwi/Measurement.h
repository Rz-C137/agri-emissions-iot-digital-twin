#pragma once
#include <cstdint>
#include <cmath>

struct Measurement {
    uint32_t sequence = 0;
    uint64_t uptime_ms = 0;
    int64_t epoch_s = 0;
    float temperature_c = NAN;
    float relative_humidity_pct = NAN;
    uint16_t gas_raw = 0;
    bool environmental_sensor_ok = false;
    // ADC conversion is observable; the analog instrument's health is not.
    bool gas_acquired = false;
    bool network_ok = false;
    bool storage_ok = false;
    bool buffered = false;
    uint8_t quality = 0;
};

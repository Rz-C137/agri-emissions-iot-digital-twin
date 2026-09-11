#pragma once
#include <cstdint>
#include <cmath>

struct Measurement {
    uint32_t sequence = 0;
    uint64_t uptime_ms = 0;
    int64_t epoch_s = 0;
    float temperature_c = NAN;
    float relative_humidity_pct = NAN;
    float co2_ppm = NAN;
    float temperature_dht22_c = NAN;
    float temperature_ds18b20_c = NAN;
    float temperature_bmp180_c = NAN;
    float pressure_hpa = NAN;
    float temp_delta_dht_ds18_c = NAN;
    float temp_delta_dht_bmp_c = NAN;
    float temp_max_disagreement_c = NAN;
    char suspected_sensor[12] = "NONE";
    uint16_t gas_raw = 0;
    bool environmental_sensor_ok = false;
    bool gas_acquired = false;
    bool temp_sensor_disagreement = false;
    bool network_ok = false;
    bool storage_ok = false;
    bool buffered = false;
    uint8_t quality = 0;
};

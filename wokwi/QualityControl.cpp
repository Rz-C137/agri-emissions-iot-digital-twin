#include "QualityControl.h"
#include <algorithm>
#include <cmath>
#include <cstring>

namespace {
bool finite(float value) { return std::isfinite(value); }

float median3(float a, float b, float c) {
    if (a > b) std::swap(a, b);
    if (b > c) std::swap(b, c);
    if (a > b) std::swap(a, b);
    return b;
}

void setSuspect(Measurement& m, const char* name) {
    std::strncpy(m.suspected_sensor, name, sizeof(m.suspected_sensor) - 1);
    m.suspected_sensor[sizeof(m.suspected_sensor) - 1] = '\0';
}
}  // namespace

void QualityControl::applyTemperatureAgreement(Measurement& m, float threshold_c) {
    m.temp_sensor_disagreement = false;
    setSuspect(m, "NONE");
    m.temp_delta_dht_ds18_c = NAN;
    m.temp_delta_dht_bmp_c = NAN;
    m.temp_max_disagreement_c = NAN;

    const bool hasDht = finite(m.temperature_dht22_c);
    const bool hasDs18 = finite(m.temperature_ds18b20_c);
    const bool hasBmp = finite(m.temperature_bmp180_c);
    if (!hasDht && !hasDs18 && !hasBmp) return;

    if (hasDht && hasDs18)
        m.temp_delta_dht_ds18_c = std::fabs(m.temperature_dht22_c - m.temperature_ds18b20_c);
    if (hasDht && hasBmp)
        m.temp_delta_dht_bmp_c = std::fabs(m.temperature_dht22_c - m.temperature_bmp180_c);

    float maxDelta = 0.0f;
    if (finite(m.temp_delta_dht_ds18_c)) maxDelta = std::max(maxDelta, m.temp_delta_dht_ds18_c);
    if (finite(m.temp_delta_dht_bmp_c)) maxDelta = std::max(maxDelta, m.temp_delta_dht_bmp_c);
    if (hasDs18 && hasBmp)
        maxDelta = std::max(maxDelta, std::fabs(m.temperature_ds18b20_c - m.temperature_bmp180_c));
    m.temp_max_disagreement_c = maxDelta;

    if (maxDelta <= threshold_c) return;

    m.temp_sensor_disagreement = true;
    if (hasDht && hasDs18 && hasBmp) {
        const float ref = median3(m.temperature_dht22_c, m.temperature_ds18b20_c, m.temperature_bmp180_c);
        const float dDht = std::fabs(m.temperature_dht22_c - ref);
        const float dDs18 = std::fabs(m.temperature_ds18b20_c - ref);
        const float dBmp = std::fabs(m.temperature_bmp180_c - ref);
        if (dDht >= dDs18 && dDht >= dBmp)
            setSuspect(m, "DHT22");
        else if (dDs18 >= dBmp)
            setSuspect(m, "DS18B20");
        else
            setSuspect(m, "BMP180");
    } else if (hasDht && hasDs18) {
        const float mid = (m.temperature_dht22_c + m.temperature_ds18b20_c) / 2.0f;
        setSuspect(m, std::fabs(m.temperature_dht22_c - mid) >= std::fabs(m.temperature_ds18b20_c - mid)
                       ? "DHT22"
                       : "DS18B20");
    } else if (hasDht && hasBmp) {
        const float mid = (m.temperature_dht22_c + m.temperature_bmp180_c) / 2.0f;
        setSuspect(m, std::fabs(m.temperature_dht22_c - mid) >= std::fabs(m.temperature_bmp180_c - mid)
                       ? "DHT22"
                       : "BMP180");
    } else if (hasDs18 && hasBmp) {
        const float mid = (m.temperature_ds18b20_c + m.temperature_bmp180_c) / 2.0f;
        setSuspect(m, std::fabs(m.temperature_ds18b20_c - mid) >= std::fabs(m.temperature_bmp180_c - mid)
                       ? "DS18B20"
                       : "BMP180");
    }
}

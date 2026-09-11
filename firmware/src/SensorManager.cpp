#include "SensorManager.h"
#include "QualityControl.h"
#include <Arduino.h>
#include <esp_timer.h>
#include <time.h>

void SensorManager::begin() {
#if AGRI_ENABLE_SCD41
    scd41_.begin();
#else
    dht22_.begin();
#endif
    ds18_.begin();
    bmp180_.begin();
    gas_.begin();
}

Measurement SensorManager::acquire(uint32_t sequence) {
    Measurement m;
    m.sequence = sequence;
    m.uptime_ms = esp_timer_get_time() / 1000;
    const auto now = time(nullptr);
    m.epoch_s = now > 1700000000 ? now : 0;

#if AGRI_ENABLE_SCD41
    const Scd41Sample scd = scd41_.read();
    if (scd.ok) {
        m.temperature_dht22_c = scd.temperature_c;
        m.temperature_c = scd.temperature_c;
        m.relative_humidity_pct = scd.relative_humidity_pct;
        m.co2_ppm = scd.co2_ppm;
        m.environmental_sensor_ok = true;
    }
#else
    float rh = NAN;
    if (dht22_.read(m.temperature_dht22_c, rh)) {
        m.temperature_c = m.temperature_dht22_c;
        m.relative_humidity_pct = rh;
    }
#endif

    ds18_.read(m.temperature_ds18b20_c);
    float pressure = NAN;
    if (bmp180_.read(m.temperature_bmp180_c, pressure)) m.pressure_hpa = pressure;

    if (!std::isfinite(m.temperature_c) && std::isfinite(m.temperature_ds18b20_c))
        m.temperature_c = m.temperature_ds18b20_c;
    else if (!std::isfinite(m.temperature_c) && std::isfinite(m.temperature_bmp180_c))
        m.temperature_c = m.temperature_bmp180_c;

    m.gas_acquired = gas_.read(m.gas_raw);
    m.environmental_sensor_ok =
        std::isfinite(m.temperature_c) && std::isfinite(m.relative_humidity_pct);

    QualityControl::applyTemperatureAgreement(m, Config::TEMP_DISAGREEMENT_THRESHOLD_C);
    return m;
}

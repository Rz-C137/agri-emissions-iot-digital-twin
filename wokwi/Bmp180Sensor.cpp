#include "Bmp180Sensor.h"
#include "Config.h"
#include <Wire.h>
#include <cmath>

bool Bmp180Sensor::begin() {
    Wire.begin(Config::I2C_SDA, Config::I2C_SCL);
    return bmp_.begin();
}

bool Bmp180Sensor::read(float& temperature_c, float& pressure_hpa) {
    temperature_c = bmp_.readTemperature();
    const int32_t pressure_pa = bmp_.readPressure();
    pressure_hpa = static_cast<float>(pressure_pa) / 100.0f;
    return std::isfinite(temperature_c) && std::isfinite(pressure_hpa) && pressure_hpa > 0.0f;
}

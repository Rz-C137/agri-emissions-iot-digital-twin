#include "Ds18b20Sensor.h"
#include <cmath>

void Ds18b20Sensor::begin() {
    sensors_.begin();
    sensors_.setWaitForConversion(true);
}

bool Ds18b20Sensor::read(float& temperature_c) {
    sensors_.requestTemperatures();
    temperature_c = sensors_.getTempCByIndex(0);
    return std::isfinite(temperature_c) && temperature_c > -100.0f;
}

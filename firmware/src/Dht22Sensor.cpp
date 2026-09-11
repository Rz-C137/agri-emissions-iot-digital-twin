#include "Dht22Sensor.h"
#include <cmath>

void Dht22Sensor::begin() { dht_.begin(); }

bool Dht22Sensor::read(float& temperature_c, float& relative_humidity_pct) {
    temperature_c = dht_.readTemperature();
    relative_humidity_pct = dht_.readHumidity();
    return std::isfinite(temperature_c) && std::isfinite(relative_humidity_pct);
}

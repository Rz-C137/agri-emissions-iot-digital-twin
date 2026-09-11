#pragma once
#include "Config.h"
#include <DHT.h>

class Dht22Sensor {
    DHT dht_{Config::DHT_PIN, DHT22};

public:
    void begin();
    bool read(float& temperature_c, float& relative_humidity_pct);
};

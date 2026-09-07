#pragma once
#include <DHT.h>
#include "Config.h"
#include "Measurement.h"

class Sensors {
    DHT dht{Config::DHT_PIN, DHT22};
public:
    void begin();
    Measurement acquire(uint32_t sequence);
};

#pragma once
#include "Config.h"
#include <DallasTemperature.h>
#include <OneWire.h>

class Ds18b20Sensor {
    OneWire wire_{Config::DS18B20_PIN};
    DallasTemperature sensors_{&wire_};

public:
    void begin();
    bool read(float& temperature_c);
};

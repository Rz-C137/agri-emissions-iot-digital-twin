#pragma once
#include "Config.h"
#include <cstdint>

class AnalogGasSensor {
public:
    void begin();
    bool read(uint16_t& raw);
};

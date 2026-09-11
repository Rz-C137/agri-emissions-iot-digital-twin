#include "AnalogGasSensor.h"
#include <Arduino.h>

void AnalogGasSensor::begin() { analogReadResolution(12); }

bool AnalogGasSensor::read(uint16_t& raw) {
    raw = static_cast<uint16_t>(analogRead(Config::GAS_PIN));
    return true;
}

#pragma once
#include <Arduino.h>
#include "SystemState.h"

namespace FaultManager {
inline void event(const char* severity, const char* message) {
    Serial.printf("# EVENT,%lu,%s,%s\n", millis(), severity, message);
}
inline void sensorFailure(SystemState& state) {
    state.sensor_failures++;
    event("ERROR", "Sensor communication failed; acquisition retry at next sample");
}
}

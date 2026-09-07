#pragma once
#include <Arduino.h>
#include "Measurement.h"

class Logger {
public:
    bool begin();
    bool append(const Measurement& m);
    static String csv(const Measurement& m);
};

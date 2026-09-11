#pragma once
#include <Adafruit_BMP085.h>

class Bmp180Sensor {
    Adafruit_BMP085 bmp_;

public:
    bool begin();
    bool read(float& temperature_c, float& pressure_hpa);
};

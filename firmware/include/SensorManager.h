#pragma once
#include "AnalogGasSensor.h"
#include "Bmp180Sensor.h"
#include "Config.h"
#include "Ds18b20Sensor.h"
#include "Measurement.h"
#if AGRI_ENABLE_SCD41
#include "Scd41.h"
#else
#include "Dht22Sensor.h"
#endif

class SensorManager {
#if AGRI_ENABLE_SCD41
    Scd41 scd41_;
#else
    Dht22Sensor dht22_;
#endif
    Ds18b20Sensor ds18_;
    Bmp180Sensor bmp180_;
    AnalogGasSensor gas_;

public:
    void begin();
    Measurement acquire(uint32_t sequence);
};

#pragma once
#include <WiFi.h>
#include <PubSubClient.h>
#include "Config.h"
#include "Measurement.h"
#include "SystemState.h"

class Telemetry {
    WiFiClient socket;
    PubSubClient mqtt{socket};
    Measurement queue[Config::QUEUE_SIZE];
    size_t head = 0, count = 0;
    uint32_t lastAttempt = 0;
public:
    void begin();
    bool enqueue(const Measurement& m);
    void service(SystemState& state);
};

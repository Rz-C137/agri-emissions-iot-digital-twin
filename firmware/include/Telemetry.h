#pragma once
#include <WiFi.h>
#include <PubSubClient.h>
#include "Config.h"
#include "Measurement.h"
#include "SystemState.h"
#include "RecordQueue.h"

class Telemetry {
    WiFiClient socket;
    PubSubClient mqtt{socket};
    RecordQueue<Config::QUEUE_SIZE> queue;
    uint32_t lastAttempt = 0;
public:
    void begin();
    bool enqueue(const Measurement& m);
    void service(SystemState& state);
};

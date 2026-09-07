#include <Arduino.h>
#include "Config.h"
#include "Sensors.h"
#include "Quality.h"
#include "Logger.h"
#include "Telemetry.h"
#include "FaultManager.h"

Sensors sensors;
Logger logger;
Telemetry telemetry;
SystemState state;
uint32_t lastSample = 0, lastStorageRetry = 0, sequence = 0;

void setup() {
    Serial.begin(115200);
    pinMode(Config::LED_PIN, OUTPUT);
    sensors.begin();
    state.storage = logger.begin();
    telemetry.begin();
    configTime(0, 0, "pool.ntp.org");
    FaultManager::event(state.storage ? "INFO" : "ERROR", state.storage ? "SD initialized" : "SD initialization failed");
    FaultManager::event("INFO", "Virtual surrogate acquisition; MQ2 is not selective NH3");
}
void loop() {
    const uint32_t now = millis();
    // Acquisition is scheduled before telemetry so outages do not gate local measurement attempts.
    if (now - lastSample >= Config::SAMPLE_MS) {
        lastSample = now;
        auto m = sensors.acquire(sequence++);
        m.quality = Quality::evaluate(m);
        m.network_ok = state.network;
        m.storage_ok = state.storage;
        m.buffered = !state.network;
        if (!m.environmental_sensor_ok) FaultManager::sensorFailure(state);
        if (state.storage && !logger.append(m)) state.storage = false;
        m.storage_ok = state.storage;
        if (!state.storage) FaultManager::event("ERROR", "Local write unavailable; telemetry queue attempt follows; record is not durable");
        if (!telemetry.enqueue(m)) {
            state.queue_overflows++;
            FaultManager::event("ERROR", "Telemetry queue full; new record rejected; SD copy exists only if local write succeeded");
        }
        Serial.println(Logger::csv(m));
        digitalWrite(Config::LED_PIN, m.environmental_sensor_ok && state.storage);
    }
    if (!state.storage && now - lastStorageRetry >= Config::RETRY_MS) {
        lastStorageRetry = now;
        state.storage = logger.begin();
        if (state.storage) FaultManager::event("INFO", "Storage reinitialized; future local writes resumed");
    }
    telemetry.service(state);
    delay(1);
}

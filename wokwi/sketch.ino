#include <Arduino.h>
#include "Config.h"
#include "Sensors.h"
#include "Quality.h"
#include "Logger.h"
#include "Telemetry.h"
#include "FaultManager.h"
#if AGRI_ENABLE_RS485
#include "Rs485Transport.h"
Rs485Transport referenceBus;
#endif

Sensors sensors;
Logger logger;
Telemetry telemetry;
SystemState state;
uint32_t lastSample = 0, lastStorageRetry = 0, sequence = 0;

void setup() {
    Serial.begin(115200);
    pinMode(Config::LED_PIN, OUTPUT);
    sensors.begin();
#if AGRI_ENABLE_RS485
    referenceBus.begin(Config::RS485_BAUD, SERIAL_8E1);
#endif
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
#if AGRI_ENABLE_RS485
        const auto reference = ModbusRtu::poll(referenceBus, Config::RS485_TIMEOUT_MS);
        Serial.printf("# MODBUS_REFERENCE,sequence=%lu,status=%s", static_cast<unsigned long>(m.sequence), ModbusRtu::statusName(reference.status));
        if (reference.status == ModbusRtu::Status::OK)
            Serial.printf(",nh3_ppm=%.2f,ch4_ppm=%.2f,n2o_ppm=%.3f", reference.nh3, reference.ch4, reference.n2o);
        Serial.println();
#endif
    }
    if (!state.storage && now - lastStorageRetry >= Config::RETRY_MS) {
        lastStorageRetry = now;
        state.storage = logger.begin();
        if (state.storage) FaultManager::event("INFO", "Storage reinitialized; future local writes resumed");
    }
    telemetry.service(state);
    delay(1);
}

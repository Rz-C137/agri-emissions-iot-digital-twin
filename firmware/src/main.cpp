#include <Arduino.h>
#include "Config.h"
#include "SensorManager.h"
#include "Quality.h"
#include "Logger.h"
#include "Telemetry.h"
#include "FaultManager.h"
#if AGRI_ENABLE_RS485
#include "Rs485Transport.h"
Rs485Transport referenceBus;
#endif

SensorManager sensors;
Logger logger;
Telemetry telemetry;
SystemState state;
uint32_t lastSample = 0, lastStorageRetry = 0, sequence = 0;

void logTemperatureQc(const Measurement& m) {
    Serial.printf(
        "# TEMP_QC,dht=%.2f,ds18=%.2f,bmp=%.2f,max_delta=%.2f,status=%s,suspect=%s\n",
        m.temperature_dht22_c, m.temperature_ds18b20_c, m.temperature_bmp180_c,
        m.temp_max_disagreement_c, m.temp_sensor_disagreement ? "WARNING" : "PASS",
        m.suspected_sensor);
}

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
    FaultManager::event(state.storage ? "INFO" : "ERROR",
                        state.storage ? "SD initialized" : "SD initialization failed");
    FaultManager::event("INFO", "Hero node: multi-temperature QA/QC enabled");
}
void loop() {
    const uint32_t now = millis();
    if (now - lastSample >= Config::SAMPLE_MS) {
        lastSample = now;
        auto m = sensors.acquire(sequence++);
        m.quality = Quality::evaluate(m);
        m.network_ok = state.network;
        m.storage_ok = state.storage;
        m.buffered = !state.network;
        if (!m.environmental_sensor_ok) FaultManager::sensorFailure(state);
        if (m.temp_sensor_disagreement)
            FaultManager::event("WARNING", "TEMP_SENSOR_DISAGREEMENT");
        if (state.storage && !logger.append(m)) state.storage = false;
        m.storage_ok = state.storage;
        if (!state.storage)
            FaultManager::event("ERROR",
                                "Local write unavailable; telemetry queue attempt follows");
        if (!telemetry.enqueue(m)) {
            state.queue_overflows++;
            FaultManager::event("ERROR", "Telemetry queue full; record rejected");
        }
        Serial.println(Logger::csv(m));
        logTemperatureQc(m);
        digitalWrite(Config::LED_PIN, m.environmental_sensor_ok && state.storage &&
                                           !m.temp_sensor_disagreement);
#if AGRI_ENABLE_RS485
        const auto reference = ModbusRtu::poll(referenceBus, Config::RS485_TIMEOUT_MS);
        Serial.printf("# MODBUS_REFERENCE,sequence=%lu,status=%s",
                      static_cast<unsigned long>(m.sequence),
                      ModbusRtu::statusName(reference.status));
        if (reference.status == ModbusRtu::Status::OK)
            Serial.printf(",nh3_ppm=%.2f,ch4_ppm=%.2f,n2o_ppm=%.3f", reference.nh3,
                          reference.ch4, reference.n2o);
        Serial.println();
#endif
    }
    if (!state.storage && now - lastStorageRetry >= Config::RETRY_MS) {
        lastStorageRetry = now;
        state.storage = logger.begin();
        if (state.storage) FaultManager::event("INFO", "Storage reinitialized");
    }
    telemetry.service(state);
    delay(1);
}

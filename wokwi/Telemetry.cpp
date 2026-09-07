#include "Telemetry.h"
#include "FaultManager.h"

#if __has_include("secrets.h")
#include "secrets.h"
#else
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""
#define MQTT_HOST ""
#define MQTT_PORT 1883
#endif

void Telemetry::begin() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    mqtt.setServer(MQTT_HOST, MQTT_PORT);
    mqtt.setBufferSize(1024);
    mqtt.setSocketTimeout(1);
}
bool Telemetry::enqueue(const Measurement& m) {
    if (count == Config::QUEUE_SIZE) return false;
    queue[(head + count) % Config::QUEUE_SIZE] = m;
    count++;
    return true;
}
void Telemetry::service(SystemState& state) {
    const uint32_t now = millis();
    if (now - lastAttempt >= Config::RETRY_MS) {
        lastAttempt = now;
        if (WiFi.status() != WL_CONNECTED) WiFi.reconnect();
        else if (!mqtt.connected() && strlen(MQTT_HOST)) mqtt.connect(Config::NODE);
    }
    mqtt.loop();
    const bool connected = mqtt.connected();
    if (connected != state.network)
        FaultManager::event(connected ? "INFO" : "WARNING", connected ? "MQTT recovered" : "MQTT offline");
    state.network = connected;
    // Drain one item per service call. PubSubClient publish is QoS 0, not a broker acknowledgement.
    if (!connected || !count) return;
    const Measurement& m = queue[head];
    char payload[900], t[24], h[24];
    if (std::isfinite(m.temperature_c)) snprintf(t, sizeof(t), "%.3f", m.temperature_c);
    else strcpy(t, "null");
    if (std::isfinite(m.relative_humidity_pct)) snprintf(h, sizeof(h), "%.3f", m.relative_humidity_pct);
    else strcpy(h, "null");
    snprintf(payload, sizeof(payload),
        "{\"node_id\":\"%s\",\"sequence\":%lu,\"timestamp\":%lld,\"uptime_ms\":%llu,"
        "\"temperature_c\":%s,\"relative_humidity_pct\":%s,\"gas_raw\":%u,"
        "\"nh3_raw_ppm\":null,\"nh3_calibrated_ppm\":null,\"nh3_reference_ppm\":null,"
        "\"sensor_status\":\"%s\",\"network_status\":\"%s\",\"storage_status\":\"%s\","
        "\"quality_flag\":%u,\"buffered\":%s,\"scenario\":\"WOKWI_SURROGATE\",\"simulated\":true}",
        Config::NODE, static_cast<unsigned long>(m.sequence), m.epoch_s, m.uptime_ms, t, h,
        m.gas_raw, m.sensor_ok ? "OK" : "ERROR", m.network_ok ? "ONLINE" : "OFFLINE",
        m.storage_ok ? "OK" : "FAILED", m.quality, m.buffered ? "true" : "false");
    if (mqtt.publish(Config::TOPIC, payload)) { head = (head + 1) % Config::QUEUE_SIZE; count--; }
}

#include "Telemetry.h"
#include "FaultManager.h"
#include "Serialization.h"

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
    mqtt.setBufferSize(1280);
    mqtt.setSocketTimeout(1);
}
bool Telemetry::enqueue(const Measurement& m) {
    return queue.push(m);
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
    if (!connected || !queue.front()) return;
    char payload[1024];
    if (!Serialization::json(*queue.front(), Config::NODE, payload, sizeof(payload))) {
        FaultManager::event("ERROR", "Telemetry serialization overflow; record retained");
        return;
    }
    if (mqtt.publish(Config::TOPIC, payload)) queue.pop();
}

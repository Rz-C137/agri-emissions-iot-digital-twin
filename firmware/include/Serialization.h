#pragma once
#include "Measurement.h"
#include "Quality.h"
#include <cstdio>
#include <ctime>

namespace Serialization {
inline bool timestamp(const Measurement& m, char* out, size_t capacity) {
    if (capacity) out[0] = '\0';
    if (m.epoch_s <= 0) return false;
    const std::time_t epoch = static_cast<std::time_t>(m.epoch_s);
    const auto* utc = std::gmtime(&epoch);
    return utc && std::strftime(out, capacity, "%Y-%m-%dT%H:%M:%SZ", utc) > 0;
}
inline const char* sensorStatus(const Measurement& m) {
    return m.environmental_sensor_ok && m.gas_acquired ? "UNVERIFIED" : "DEGRADED";
}
inline const char* gasStatus(const Measurement& m) { return m.gas_acquired ? "UNVERIFIED" : "MISSING"; }
inline bool json(const Measurement& m, const char* node, char* out, size_t capacity) {
    char t[24], h[24], gas[16], utc[32], timeValue[36], flags[100];
    const bool synced = timestamp(m, utc, sizeof(utc));
    if (synced) std::snprintf(timeValue, sizeof(timeValue), "\"%s\"", utc);
    else std::snprintf(timeValue, sizeof(timeValue), "null");
    if (std::isfinite(m.temperature_c)) std::snprintf(t, sizeof(t), "%.3f", m.temperature_c);
    else std::snprintf(t, sizeof(t), "null");
    if (std::isfinite(m.relative_humidity_pct)) std::snprintf(h, sizeof(h), "%.3f", m.relative_humidity_pct);
    else std::snprintf(h, sizeof(h), "null");
    if (m.gas_acquired) std::snprintf(gas, sizeof(gas), "%u", m.gas_raw);
    else std::snprintf(gas, sizeof(gas), "null");
    Quality::names(m.quality, flags, sizeof(flags));
    // Node is a compile-time identifier containing only letters, digits and hyphens.
    const int length = std::snprintf(out, capacity,
        "{\"node_id\":\"%s\",\"sequence\":%lu,\"timestamp\":%s,\"timestamp_status\":\"%s\","
        "\"uptime_ms\":%llu,\"temperature_c\":%s,\"relative_humidity_pct\":%s,\"gas_raw\":%s,"
        "\"nh3_raw_ppm\":null,\"nh3_calibrated_ppm\":null,\"nh3_reference_ppm\":null,"
        "\"environmental_sensor_status\":\"%s\",\"gas_channel_status\":\"%s\",\"sensor_status\":\"%s\","
        "\"network_status\":\"%s\",\"storage_status\":\"%s\",\"quality_code\":%u,\"quality_flags\":\"%s\","
        "\"buffered\":%s,\"scenario\":\"WOKWI_SURROGATE\",\"simulated\":true}",
        node, static_cast<unsigned long>(m.sequence), timeValue, synced ? "NTP_UTC" : "UNSYNCHRONIZED",
        static_cast<unsigned long long>(m.uptime_ms), t, h, gas,
        m.environmental_sensor_ok ? "OK" : "ERROR", gasStatus(m), sensorStatus(m),
        m.network_ok ? "ONLINE" : "OFFLINE", m.storage_ok ? "OK" : "FAILED",
        m.quality, flags, m.buffered ? "true" : "false");
    return length >= 0 && static_cast<size_t>(length) < capacity;
}
}

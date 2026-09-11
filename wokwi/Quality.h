#pragma once
#include "Measurement.h"
#include <cstdio>
#include <cstring>

namespace Quality {
enum Flag : uint8_t {
    VALID = 0,
    MISSING = 1,
    RANGE = 2,
    COMMUNICATION = 4,
    INVALID = 8,
    ABRUPT = 16,
    STALE = 32,
    OUTLIER = 64,
    TEMP_DISAGREEMENT = 128,
};

inline uint8_t evaluate(const Measurement& m) {
    uint8_t flags = m.environmental_sensor_ok ? VALID : COMMUNICATION;
    if (!std::isfinite(m.temperature_c) || !std::isfinite(m.relative_humidity_pct) || !m.gas_acquired)
        flags |= MISSING;
    if ((std::isfinite(m.temperature_c) && (m.temperature_c < -20 || m.temperature_c > 60)) ||
        (std::isfinite(m.relative_humidity_pct) &&
         (m.relative_humidity_pct < 0 || m.relative_humidity_pct > 100)) ||
        (m.gas_acquired && m.gas_raw > 4095))
        flags |= RANGE;
    if (m.temp_sensor_disagreement) flags |= TEMP_DISAGREEMENT;
    return flags;
}

inline void names(uint8_t code, char* out, size_t capacity) {
    const char* labels[] = {"MISSING",       "RANGE",       "COMMUNICATION", "INVALID",
                            "ABRUPT",        "STALE",       "OUTLIER",       "TEMP_DISAGREEMENT"};
    if (!capacity) return;
    out[0] = '\0';
    if (!code) {
        std::snprintf(out, capacity, "VALID");
        return;
    }
    for (unsigned i = 0; i < 8; ++i) {
        if (code & (1u << i)) {
            const size_t used = std::strlen(out);
            if (used < capacity)
                std::snprintf(out + used, capacity - used, "%s%s", used ? "|" : "", labels[i]);
        }
    }
}
}  // namespace Quality

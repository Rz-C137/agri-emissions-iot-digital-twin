#pragma once
#include "Measurement.h"

namespace Quality {
enum Flag : uint8_t { VALID = 0, MISSING = 1, RANGE = 2, COMMUNICATION = 4 };
inline uint8_t evaluate(const Measurement& m) {
    uint8_t flags = m.sensor_ok ? VALID : COMMUNICATION;
    if (!std::isfinite(m.temperature_c) || !std::isfinite(m.relative_humidity_pct))
        flags |= MISSING;
    if ((std::isfinite(m.temperature_c) && (m.temperature_c < -20 || m.temperature_c > 60)) ||
        (std::isfinite(m.relative_humidity_pct) &&
         (m.relative_humidity_pct < 0 || m.relative_humidity_pct > 100)) || m.gas_raw > 4095)
        flags |= RANGE;
    return flags;
}
}

#pragma once
#include <cstdint>

struct SystemState {
    bool network = false;
    bool storage = false;
    uint32_t sensor_failures = 0;
    uint32_t queue_overflows = 0;
};

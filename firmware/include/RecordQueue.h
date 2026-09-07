#pragma once
#include <cstddef>
#include "Measurement.h"

template<size_t Capacity> class RecordQueue {
    static_assert(Capacity > 0, "Queue must have capacity");
    Measurement records[Capacity];
    size_t head = 0, count = 0;
public:
    bool push(const Measurement& record) {
        if (count == Capacity) return false; // Reject new record; never replace an older pending record.
        records[(head + count) % Capacity] = record;
        ++count;
        return true;
    }
    const Measurement* front() const { return count ? &records[head] : nullptr; }
    void pop() { if (count) { head = (head + 1) % Capacity; --count; } }
};

#include "Quality.h"
#include "Serialization.h"
#include "RecordQueue.h"
#include <cassert>
#include <cstring>
#include <iostream>

int main() {
    Measurement m;
    assert(Quality::evaluate(m) == (Quality::MISSING | Quality::COMMUNICATION));
    m.environmental_sensor_ok = true;
    m.gas_acquired = true;
    m.temperature_c = 22;
    m.relative_humidity_pct = 65;
    assert(Quality::evaluate(m) == Quality::VALID);
    assert(std::strcmp(Serialization::sensorStatus(m), "UNVERIFIED") == 0);
    m.relative_humidity_pct = 101;
    assert(Quality::evaluate(m) & Quality::RANGE);
    char names[100];
    Quality::names(5, names, sizeof(names));
    assert(std::strcmp(names, "MISSING|COMMUNICATION") == 0);
    RecordQueue<2> queue;
    m.sequence = 1; assert(queue.push(m));
    m.sequence = 2; assert(queue.push(m));
    m.sequence = 3; assert(!queue.push(m));
    assert(queue.front()->sequence == 1);
    queue.pop(); assert(queue.push(m));
    assert(queue.front()->sequence == 2);
    queue.pop(); assert(queue.front()->sequence == 3);
    queue.pop(); assert(!queue.front());
    m = Measurement{};
    m.quality = Quality::evaluate(m);
    char json[1024];
    assert(Serialization::json(m, "test-node", json, sizeof(json)));
    assert(std::strstr(json, "\"timestamp\":null"));
    assert(std::strstr(json, "UNSYNCHRONIZED"));
    assert(!std::strstr(json, "nan"));
    std::cout << json << '\n';
    m.epoch_s = 1767225600;
    assert(Serialization::json(m, "test-node", json, sizeof(json)));
    assert(std::strstr(json, "2026-01-01T00:00:00Z"));
    assert(!Serialization::json(m, "test-node", json, 8));
}

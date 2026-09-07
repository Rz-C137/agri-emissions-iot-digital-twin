#include "Quality.h"
#include <cassert>

int main() {
    Measurement m;
    assert(Quality::evaluate(m) & Quality::MISSING);
    m.sensor_ok = true;
    m.temperature_c = 22;
    m.relative_humidity_pct = 65;
    assert(Quality::evaluate(m) == Quality::VALID);
    m.relative_humidity_pct = 101;
    assert(Quality::evaluate(m) & Quality::RANGE);
}

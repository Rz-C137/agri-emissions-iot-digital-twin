#pragma once
#include <cmath>
#include <cstdint>

struct Scd41Sample {
    bool ok = false;
    float co2_ppm = NAN;
    float temperature_c = NAN;
    float relative_humidity_pct = NAN;
};

class Scd41 {
public:
    bool begin();
    Scd41Sample read(uint16_t timeout_ms = 1200);

private:
    static constexpr uint8_t ADDRESS = 0x62;
    bool writeCommand(uint16_t command);
    bool readResponse(uint8_t* data, size_t len);
    static uint8_t crc8(const uint8_t* data, size_t len);
    static bool verifyWord(const uint8_t* word);
    static float decodeCo2(uint16_t raw);
    static float decodeTemperature(uint16_t raw);
    static float decodeHumidity(uint16_t raw);
};

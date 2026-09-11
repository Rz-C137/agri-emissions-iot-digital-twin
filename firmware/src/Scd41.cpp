#include "Scd41.h"
#include "Config.h"
#include <Arduino.h>
#include <Wire.h>
#include <cmath>

namespace {
constexpr uint16_t CMD_STOP_PERIODIC = 0x3F86;
constexpr uint16_t CMD_START_PERIODIC = 0x21B1;
constexpr uint16_t CMD_READ_MEASUREMENT = 0xEC05;
constexpr uint16_t CMD_GET_DATA_READY = 0xE4B8;
constexpr uint32_t STARTUP_MS = 5000;
}  // namespace

uint8_t Scd41::crc8(const uint8_t* data, size_t len) {
    uint8_t crc = 0xFF;
    for (size_t i = 0; i < len; ++i) {
        crc ^= data[i];
        for (uint8_t bit = 0; bit < 8; ++bit) {
            crc = (crc & 0x80) ? static_cast<uint8_t>((crc << 1) ^ 0x31) : static_cast<uint8_t>(crc << 1);
        }
    }
    return crc;
}

bool Scd41::verifyWord(const uint8_t* word) {
    return crc8(word, 2) == word[2];
}

float Scd41::decodeCo2(uint16_t raw) { return static_cast<float>(raw); }

float Scd41::decodeTemperature(uint16_t raw) {
    return -45.0f + 175.0f * static_cast<float>(raw) / 65535.0f;
}

float Scd41::decodeHumidity(uint16_t raw) {
    return 100.0f * static_cast<float>(raw) / 65535.0f;
}

bool Scd41::writeCommand(uint16_t command) {
    Wire.beginTransmission(ADDRESS);
    Wire.write(static_cast<uint8_t>(command >> 8));
    Wire.write(static_cast<uint8_t>(command & 0xFF));
    return Wire.endTransmission() == 0;
}

bool Scd41::readResponse(uint8_t* data, size_t len) {
    const size_t received = Wire.requestFrom(static_cast<int>(ADDRESS), static_cast<int>(len));
    if (received != len) return false;
    for (size_t i = 0; i < len; ++i) {
        if (!Wire.available()) return false;
        data[i] = static_cast<uint8_t>(Wire.read());
    }
    return true;
}

bool Scd41::begin() {
    Wire.begin(Config::I2C_SDA, Config::I2C_SCL);
    Wire.setClock(100000);
    delay(30);
    if (!writeCommand(CMD_STOP_PERIODIC)) return false;
    delay(500);
    if (!writeCommand(CMD_START_PERIODIC)) return false;
    delay(STARTUP_MS);
    return true;
}

Scd41Sample Scd41::read(uint16_t timeout_ms) {
    Scd41Sample sample;
    const uint32_t deadline = millis() + timeout_ms;
    bool ready = false;
    while (millis() < deadline) {
        if (!writeCommand(CMD_GET_DATA_READY)) {
            delay(50);
            continue;
        }
        delay(1);
        uint8_t status[3] = {0};
        if (!readResponse(status, sizeof(status)) || !verifyWord(status)) {
            delay(50);
            continue;
        }
        const uint16_t raw = static_cast<uint16_t>((status[0] << 8) | status[1]);
        if (raw & 0x07FF) {
            ready = true;
            break;
        }
        delay(50);
    }
    if (!ready) return sample;

    if (!writeCommand(CMD_READ_MEASUREMENT)) return sample;
    delay(1);
    uint8_t payload[9] = {0};
    if (!readResponse(payload, sizeof(payload))) return sample;
    if (!verifyWord(payload) || !verifyWord(payload + 3) || !verifyWord(payload + 6)) return sample;

    const uint16_t co2_raw = static_cast<uint16_t>((payload[0] << 8) | payload[1]);
    const uint16_t temp_raw = static_cast<uint16_t>((payload[3] << 8) | payload[4]);
    const uint16_t rh_raw = static_cast<uint16_t>((payload[6] << 8) | payload[7]);

    sample.co2_ppm = decodeCo2(co2_raw);
    sample.temperature_c = decodeTemperature(temp_raw);
    sample.relative_humidity_pct = decodeHumidity(rh_raw);
    sample.ok = std::isfinite(sample.co2_ppm) && std::isfinite(sample.temperature_c) &&
                std::isfinite(sample.relative_humidity_pct);
    return sample;
}

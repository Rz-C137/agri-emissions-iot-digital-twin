#pragma once
#include <cstddef>
#include <cstdint>

#ifndef AGRI_ENABLE_RS485
#define AGRI_ENABLE_RS485 1
#endif

#ifndef AGRI_ENABLE_SCD41
#define AGRI_ENABLE_SCD41 0
#endif

namespace Config {
constexpr uint8_t DHT_PIN = 4;
constexpr uint8_t DS18B20_PIN = 15;
constexpr uint8_t GAS_PIN = 34;
constexpr uint8_t SD_CS = 5;
constexpr uint8_t LED_PIN = 2;
constexpr uint8_t I2C_SDA = 21;
constexpr uint8_t I2C_SCL = 22;
constexpr uint8_t RS485_TX = 17;
constexpr uint8_t RS485_RX = 16;
constexpr uint8_t RS485_DIRECTION = 27;
constexpr uint32_t RS485_BAUD = 9600;
constexpr uint32_t RS485_TIMEOUT_MS = 250;
constexpr uint32_t SAMPLE_MS = 5000;
constexpr uint32_t RETRY_MS = 10000;
constexpr float TEMP_DISAGREEMENT_THRESHOLD_C = 1.0f;
constexpr size_t QUEUE_SIZE = 120;
constexpr const char* NODE = "esp32-hero-01";
constexpr const char* TOPIC = "agri/hero/telemetry";
}  // namespace Config

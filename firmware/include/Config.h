#pragma once
#include <cstddef>
#include <cstdint>

#ifndef AGRI_ENABLE_RS485
#define AGRI_ENABLE_RS485 0
#endif

namespace Config {
constexpr uint8_t DHT_PIN = 4, GAS_PIN = 34, SD_CS = 5, LED_PIN = 2;
constexpr uint8_t RS485_TX = 17, RS485_RX = 16, RS485_DIRECTION = 27;
constexpr uint32_t RS485_BAUD = 9600, RS485_TIMEOUT_MS = 250;
constexpr uint32_t SAMPLE_MS = 5000, RETRY_MS = 10000;
constexpr size_t QUEUE_SIZE = 120;
constexpr const char* NODE = "esp32-surrogate-01";
constexpr const char* TOPIC = "agri/virtual/telemetry";
}

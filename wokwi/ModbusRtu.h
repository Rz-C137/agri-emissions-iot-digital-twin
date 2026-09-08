#pragma once
#include <array>
#include <cstdint>
#include <cstddef>
#include <limits>

// Mirror simulator/modbus.py; tests/test_modbus_contract.py locks the wire contract.
namespace ModbusRtu {
constexpr uint8_t UNIT = 1, FUNCTION = 3;
constexpr uint16_t START = 0, COUNT = 3;
constexpr size_t RESPONSE_SIZE = 11;
enum class Status { OK, TIMEOUT, LENGTH_ERROR, CRC_ERROR, UNIT_ERROR, FUNCTION_ERROR, TRANSPORT_ERROR };
struct Result {
    Status status;
    float nh3 = std::numeric_limits<float>::quiet_NaN();
    float ch4 = std::numeric_limits<float>::quiet_NaN();
    float n2o = std::numeric_limits<float>::quiet_NaN();
    explicit Result(Status s) : status(s) {}
};
uint16_t crc16(const uint8_t* data, size_t size);
std::array<uint8_t, 8> request();
Result parse(const uint8_t* data, size_t size);
const char* statusName(Status status);

class Transport {
public:
    virtual ~Transport() = default;
    // Return false on transport failure; zero received bytes represents timeout.
    // Must report oversize frames as failure, never truncate them into a valid response.
    virtual bool exchange(const uint8_t* tx, size_t txSize, uint8_t* rx,
                          size_t capacity, size_t& received, uint32_t timeoutMs) = 0;
};
Result poll(Transport& transport, uint32_t timeoutMs);
}

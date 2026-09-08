#include "ModbusRtu.h"

namespace ModbusRtu {
uint16_t crc16(const uint8_t* data, size_t size) {
    uint16_t crc = 0xffff;
    for (size_t i = 0; i < size; ++i) {
        crc ^= data[i];
        for (int bit = 0; bit < 8; ++bit)
            crc = (crc >> 1) ^ ((crc & 1) ? 0xa001 : 0);
    }
    return crc;
}
std::array<uint8_t, 8> request() {
    std::array<uint8_t, 8> bytes{{UNIT, FUNCTION, START >> 8, START & 255,
                               COUNT >> 8, COUNT & 255, 0, 0}};
    const auto crc = crc16(bytes.data(), 6);
    bytes[6] = crc & 255;
    bytes[7] = crc >> 8;
    return bytes;
}
Result parse(const uint8_t* bytes, size_t size) {
    if (!size) return Result(Status::TIMEOUT);
    if (!bytes || size != RESPONSE_SIZE) return Result(Status::LENGTH_ERROR);
    if (crc16(bytes, size - 2) != (bytes[size - 2] | uint16_t(bytes[size - 1]) << 8))
        return Result(Status::CRC_ERROR);
    if (bytes[0] != UNIT) return Result(Status::UNIT_ERROR);
    if (bytes[1] != FUNCTION) return Result(Status::FUNCTION_ERROR);
    if (bytes[2] != COUNT * 2) return Result(Status::LENGTH_ERROR);
    Result result(Status::OK);
    result.nh3 = (uint16_t(bytes[3]) << 8 | bytes[4]) / 100.0f;
    result.ch4 = (uint16_t(bytes[5]) << 8 | bytes[6]) / 100.0f;
    result.n2o = (uint16_t(bytes[7]) << 8 | bytes[8]) / 1000.0f;
    return result;
}
Result poll(Transport& transport, uint32_t timeoutMs) {
    const auto tx = request();
    uint8_t rx[RESPONSE_SIZE]{};
    size_t received = 0;
    if (!transport.exchange(tx.data(), tx.size(), rx, sizeof(rx), received, timeoutMs))
        return Result(Status::TRANSPORT_ERROR);
    return parse(rx, received);
}
const char* statusName(Status status) {
    switch (status) {
        case Status::OK: return "OK";
        case Status::TIMEOUT: return "TIMEOUT";
        case Status::LENGTH_ERROR: return "LENGTH_ERROR";
        case Status::CRC_ERROR: return "CRC_ERROR";
        case Status::UNIT_ERROR: return "UNIT_ERROR";
        case Status::FUNCTION_ERROR: return "FUNCTION_ERROR";
        default: return "TRANSPORT_ERROR";
    }
}
}

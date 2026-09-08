#include "ModbusRtu.h"
#include <cassert>
#include <cmath>
#include <cstring>
#include <cstdio>
#include <vector>
#include <cstdlib>

using namespace ModbusRtu;
std::vector<uint8_t> unhex(const char* hex) {
    std::vector<uint8_t> bytes;
    while (*hex) {
        char pair[]{hex[0], hex[1], 0};
        bytes.push_back(uint8_t(std::strtoul(pair, nullptr, 16)));
        hex += 2;
    }
    return bytes;
}
void checksum(std::vector<uint8_t>& bytes) {
    const auto crc = crc16(bytes.data(), bytes.size() - 2);
    bytes[bytes.size() - 2] = crc & 255;
    bytes.back() = crc >> 8;
}
struct Fake : Transport {
    std::vector<uint8_t> reply;
    bool fail = false;
    bool exchange(const uint8_t* tx, size_t n, uint8_t* rx, size_t cap,
                  size_t& received, uint32_t timeout) override {
        assert(n == 8 && std::memcmp(tx, request().data(), 8) == 0 && timeout == 250);
        received = reply.size();
        assert(received <= cap);
        if (received) std::memcpy(rx, reply.data(), received);
        return !fail;
    }
};
int main(int argc, char** argv) {
    assert(argc == 6);
    const auto expectedRequest = unhex(argv[1]);
    const auto valid = unhex(argv[2]);
    assert(expectedRequest.size() == 8 && valid.size() == 11);
    assert(std::memcmp(request().data(), expectedRequest.data(), 8) == 0);
    assert(crc16(reinterpret_cast<const uint8_t*>("123456789"), 9) == 0x4b37);
    auto result = parse(valid.data(), valid.size());
    assert(result.status == Status::OK);
    assert(std::fabs(result.nh3 - std::atof(argv[3])) < 0.0001);
    assert(std::fabs(result.ch4 - std::atof(argv[4])) < 0.0001);
    assert(std::fabs(result.n2o - std::atof(argv[5])) < 0.0001);
    auto bad = valid; bad.back() ^= 1;
    assert(parse(bad.data(), bad.size()).status == Status::CRC_ERROR);
    bad = valid; bad[0] = 2; checksum(bad);
    assert(parse(bad.data(), bad.size()).status == Status::UNIT_ERROR);
    bad = valid; bad[1] = 4; checksum(bad);
    assert(parse(bad.data(), bad.size()).status == Status::FUNCTION_ERROR);
    bad = valid; bad[2] = 4; checksum(bad);
    assert(parse(bad.data(), bad.size()).status == Status::LENGTH_ERROR);
    for (size_t n = 1; n < valid.size(); ++n) {
        result = parse(valid.data(), n);
        assert(result.status == Status::LENGTH_ERROR && std::isnan(result.nh3));
    }
    bad = valid; bad.push_back(0);
    assert(parse(bad.data(), bad.size()).status == Status::LENGTH_ERROR);
    Fake transport;
    transport.reply = valid;
    assert(poll(transport, 250).status == Status::OK);
    transport.reply.clear();
    result = poll(transport, 250);
    assert(result.status == Status::TIMEOUT && std::isnan(result.nh3) && std::isnan(result.ch4) && std::isnan(result.n2o));
    transport.fail = true;
    assert(poll(transport, 250).status == Status::TRANSPORT_ERROR);
    std::puts("C++ Modbus request, CRC, parsing, scaling, errors and mock transport passed");
}

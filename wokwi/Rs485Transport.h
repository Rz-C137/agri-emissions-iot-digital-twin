#pragma once
#include <Arduino.h>
#include "ModbusRtu.h"

class Rs485Transport : public ModbusRtu::Transport {
public:
    void begin(uint32_t baud = 9600, uint32_t parity = SERIAL_8E1);
    bool exchange(const uint8_t* tx, size_t txSize, uint8_t* rx,
                  size_t capacity, size_t& received, uint32_t timeoutMs) override;
private:
    uint32_t gapUs = 4011;
    bool initialized = false;
};

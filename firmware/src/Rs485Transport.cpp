#include "Rs485Transport.h"
#include "Config.h"

void Rs485Transport::begin(uint32_t baud, uint32_t parity) {
    initialized = false;
    // Only 11-bit serial characters: even/odd parity or two stop bits without parity.
    if (baud < 1200 || baud > 115200 ||
        (parity != SERIAL_8E1 && parity != SERIAL_8O1 && parity != SERIAL_8N2)) return;
    digitalWrite(Config::RS485_DIRECTION, LOW);
    pinMode(Config::RS485_DIRECTION, OUTPUT);
    Serial2.begin(baud, parity, Config::RS485_RX, Config::RS485_TX);
    gapUs = baud > 19200 ? 1750 : (38500000UL + baud - 1) / baud;
    initialized = true;
}
bool Rs485Transport::exchange(const uint8_t* tx, size_t txSize, uint8_t* rx,
                              size_t capacity, size_t& received, uint32_t timeoutMs) {
    received = 0;
    if (!initialized || !timeoutMs) return false;
    // Require a quiet interval; bounded wait also rejects a continuously busy/noisy bus.
    auto started = millis();
    auto quiet = micros();
    while (uint32_t(micros() - quiet) < gapUs) {
        if (Serial2.available()) { Serial2.read(); quiet = micros(); }
        if (uint32_t(millis() - started) >= timeoutMs) return false;
        yield();
    }
    digitalWrite(Config::RS485_DIRECTION, HIGH);
    const auto written = Serial2.write(tx, txSize);
    Serial2.flush(true); // Wait for TX completion before enabling the receiver.
    digitalWrite(Config::RS485_DIRECTION, LOW);
    if (written != txSize) return false;
    started = millis();
    auto lastByte = micros();
    while (uint32_t(millis() - started) < timeoutMs) {
        if (Serial2.available()) {
            const int value = Serial2.read();
            if (value >= 0) {
                if (received == capacity) return false;
                rx[received++] = uint8_t(value);
                lastByte = micros();
            }
        } else if (received && uint32_t(micros() - lastByte) >= gapUs) {
            return true;
        }
        yield();
    }
    // A full-size response without a completed frame gap is not accepted.
    return received < capacity;
}

#include "Logger.h"
#include "Config.h"
#include <SD.h>
#include <SPI.h>

bool Logger::begin() { return SD.begin(Config::SD_CS); }
String Logger::csv(const Measurement& m) {
    return String(static_cast<long long>(m.epoch_s)) + "," + Config::NODE + "," +
        String(m.sequence) + "," + String(static_cast<unsigned long long>(m.uptime_ms)) + "," +
        String(m.temperature_c, 3) + "," + String(m.relative_humidity_pct, 3) + "," +
        String(m.gas_raw) + ",,,," + (m.sensor_ok ? "OK" : "ERROR") + "," +
        (m.network_ok ? "ONLINE" : "OFFLINE") + "," + (m.storage_ok ? "OK" : "FAILED") +
        "," + String(m.quality) + "," + String(m.buffered) + ",WOKWI_SURROGATE,true";
}
bool Logger::append(const Measurement& m) {
    File file = SD.open("/measurements.csv", FILE_APPEND);
    if (!file) return false;
    if (!file.size()) file.println("timestamp,node_id,sequence,uptime_ms,temperature_c,relative_humidity_pct,gas_raw,nh3_raw_ppm,nh3_calibrated_ppm,nh3_reference_ppm,sensor_status,network_status,storage_status,quality_flag,buffered,scenario,simulated");
    String row = csv(m);
    bool ok = file.println(row) == row.length() + 2;
    file.flush();
    file.close();
    return ok;
}

#include "Logger.h"
#include "Config.h"
#include "Serialization.h"
#include <SD.h>
#include <SPI.h>

bool Logger::begin() { return SD.begin(Config::SD_CS); }
String Logger::csv(const Measurement& m) {
    char utc[32], flags[100];
    const bool synced = Serialization::timestamp(m, utc, sizeof(utc));
    Quality::names(m.quality, flags, sizeof(flags));
    return String(utc) + "," + (synced ? "NTP_UTC" : "UNSYNCHRONIZED") + "," + Config::NODE + "," +
        String(m.sequence) + "," + String(static_cast<unsigned long long>(m.uptime_ms)) + "," +
        (std::isfinite(m.temperature_c) ? String(m.temperature_c, 3) : String("")) + "," +
        (std::isfinite(m.relative_humidity_pct) ? String(m.relative_humidity_pct, 3) : String("")) + "," +
        (m.gas_acquired ? String(m.gas_raw) : String("")) + "," +
        (std::isfinite(m.co2_ppm) ? String(m.co2_ppm, 1) : String("")) + ",,," +
        (m.environmental_sensor_ok ? "OK" : "ERROR") + "," + Serialization::gasStatus(m) + "," +
        Serialization::sensorStatus(m) + "," + (m.network_ok ? "ONLINE" : "OFFLINE") + "," +
        (m.storage_ok ? "OK" : "FAILED") + "," + String(m.quality) + "," + flags + "," +
        String(m.buffered) + ",WOKWI_SURROGATE,true";
}
bool Logger::append(const Measurement& m) {
    File file = SD.open("/measurements-v2.csv", FILE_APPEND);
    if (!file) return false;
    if (!file.size()) file.println("timestamp,timestamp_status,node_id,sequence,uptime_ms,temperature_c,relative_humidity_pct,gas_raw,co2_ppm,nh3_calibrated_ppm,nh3_reference_ppm,environmental_sensor_status,gas_channel_status,sensor_status,network_status,storage_status,quality_code,quality_flags,buffered,scenario,simulated");
    String row = csv(m);
    bool ok = file.println(row) == row.length() + 2;
    file.flush();
    file.close();
    return ok;
}

/*
 * Agricultural IoT Emission Monitoring — Wokwi virtual hardware demo
 *
 * Hardware (see diagram.json):
 *   DHT22 DATA  -> GPIO4  (10 kΩ pull-up)
 *   Gas AO      -> GPIO34 (ADC1, simulator-only MQ-2 surrogate)
 *   microSD SPI -> CS=5, SCK=18, MISO=19, MOSI=23
 *   Status LED  -> GPIO2
 */

#include <DHT.h>
#include <SD.h>
#include <SPI.h>

#define DHT_PIN 4
#define DHT_TYPE DHT22
#define GAS_PIN 34
#define SD_CS_PIN 5
#define LED_PIN 2
#define SAMPLE_MS 5000

DHT dht(DHT_PIN, DHT_TYPE);

unsigned long lastSample = 0;
uint32_t sequence = 0;
bool sdReady = false;

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println();
  Serial.println("=== Agricultural Emission Monitoring System ===");
  Serial.println("Wokwi virtual hardware demonstrator");
  Serial.println("MQ-2 is an analog surrogate only — not selective NH3");
  Serial.println("==============================================");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  dht.begin();
  analogReadResolution(12);
  Serial.println("[OK] DHT22 initialized");

  if (SD.begin(SD_CS_PIN)) {
    sdReady = true;
    Serial.println("[OK] SD card initialized");
    File dataFile = SD.open("/data.csv", FILE_WRITE);
    if (dataFile) {
      dataFile.println("timestamp_s,sequence,temp_c,humidity_pct,gas_raw,gas_voltage_v,status");
      dataFile.close();
      Serial.println("[OK] /data.csv created");
    }
  } else {
    Serial.println("[ERROR] SD card initialization failed");
  }

  Serial.println();
  Serial.println("timestamp_s,sequence,temp_c,humidity_pct,gas_raw,gas_voltage_v,status");
  Serial.println("----------------------------------------------------------------");
}

void loop() {
  const unsigned long now = millis();
  if (now - lastSample < SAMPLE_MS) {
    delay(10);
    return;
  }
  lastSample = now;

  const float temperature = dht.readTemperature();
  const float humidity = dht.readHumidity();
  const int gasRaw = analogRead(GAS_PIN);
  const float gasVoltage = gasRaw * (3.3f / 4095.0f);
  const bool sensorOk = !isnan(temperature) && !isnan(humidity);

  digitalWrite(LED_PIN, sensorOk && sdReady ? HIGH : LOW);

  const unsigned long seconds = now / 1000;
  char line[160];
  if (sensorOk) {
    snprintf(line, sizeof(line), "%lu,%lu,%.1f,%.1f,%d,%.3f,%s",
             seconds, sequence, temperature, humidity, gasRaw, gasVoltage,
             sdReady ? "OK" : "SD_ERR");
  } else {
    snprintf(line, sizeof(line), "%lu,%lu,ERROR,ERROR,%d,%.3f,%s",
             seconds, sequence, gasRaw, gasVoltage, sdReady ? "OK" : "SD_ERR");
  }
  Serial.println(line);

  if (sdReady) {
    File dataFile = SD.open("/data.csv", FILE_APPEND);
    if (dataFile) {
      dataFile.println(line);
      dataFile.close();
    } else {
      sdReady = false;
      Serial.println("[ERROR] SD write failed");
    }
  }

  sequence++;
  if (sequence % 10 == 0) {
    Serial.println("----------------------------------------------------------------");
    Serial.printf("[INFO] %lu samples | sensor=%s | storage=%s\n",
                  sequence, sensorOk ? "OK" : "ERROR", sdReady ? "OK" : "ERROR");
    Serial.println("----------------------------------------------------------------");
  }
}

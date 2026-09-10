/*
 * Agricultural IoT Emission Monitoring System
 * Virtual Hardware Demonstration
 * 
 * Hardware:
 * - ESP32 DevKit v1
 * - DHT22 (GPIO4) - Temperature/Humidity sensor
 * - Analog Joystick (GPIO34) - Simulates gas sensor analog output
 * - microSD Card (SPI) - Local data logging
 * - Status LED (GPIO2) - System health indicator
 * 
 * Author: R. Abdollahipour
 * Purpose: ATB/MARVELA PostDoc Application Portfolio
 */

#include <DHT.h>
#include <SD.h>
#include <SPI.h>

// Pin definitions
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define GAS_ANALOG_PIN 34
#define SD_CS_PIN 5
#define LED_PIN 2

// Sensor objects
DHT dht(DHT_PIN, DHT_TYPE);

// State variables
unsigned long lastSample = 0;
const unsigned long SAMPLE_INTERVAL = 5000; // 5 seconds
int sequence = 0;
bool sdAvailable = false;

void setup() {
  Serial.begin(115200);
  Serial.println("\n=== Agricultural Emission Monitoring System ===");
  Serial.println("Virtual Hardware Demonstration");
  Serial.println("==============================================\n");
  
  // Initialize LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Initialize DHT22
  dht.begin();
  Serial.println("[OK] DHT22 initialized");
  
  // Initialize SD card
  if (SD.begin(SD_CS_PIN)) {
    sdAvailable = true;
    Serial.println("[OK] SD card initialized");
    
    // Write CSV header
    File dataFile = SD.open("/data.csv", FILE_WRITE);
    if (dataFile) {
      dataFile.println("timestamp,sequence,temp_c,humidity_pct,gas_analog_raw,gas_analog_voltage,status");
      dataFile.close();
      Serial.println("[OK] Data file created: /data.csv");
    }
  } else {
    Serial.println("[ERROR] SD card initialization failed");
  }
  
  Serial.println("\n[INFO] System ready - acquiring data every 5 seconds");
  Serial.println("timestamp,sequence,temp_c,humidity_pct,gas_raw,gas_voltage,sd_status");
  Serial.println("----------------------------------------------------------------");
}

void loop() {
  unsigned long now = millis();
  
  // Acquire data at fixed interval
  if (now - lastSample >= SAMPLE_INTERVAL) {
    lastSample = now;
    
    // Read DHT22
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    // Read analog gas sensor (simulated by joystick vertical axis)
    int gasRaw = analogRead(GAS_ANALOG_PIN);
    float gasVoltage = gasRaw * (3.3 / 4095.0);
    
    // Check sensor validity
    bool sensorOK = !isnan(temperature) && !isnan(humidity);
    
    // Update status LED (ON if all systems OK)
    digitalWrite(LED_PIN, sensorOK && sdAvailable);
    
    // Create timestamp (simulation time)
    char timestamp[32];
    unsigned long seconds = now / 1000;
    unsigned long minutes = seconds / 60;
    unsigned long hours = minutes / 60;
    sprintf(timestamp, "%02lu:%02lu:%02lu", hours % 24, minutes % 60, seconds % 60);
    
    // Format data record
    char record[256];
    if (sensorOK) {
      sprintf(record, "%s,%d,%.1f,%.1f,%d,%.3f,%s",
              timestamp, sequence, temperature, humidity, 
              gasRaw, gasVoltage, sdAvailable ? "OK" : "SD_ERR");
    } else {
      sprintf(record, "%s,%d,ERROR,ERROR,%d,%.3f,%s",
              timestamp, sequence, gasRaw, gasVoltage, 
              sdAvailable ? "OK" : "SD_ERR");
    }
    
    // Print to serial monitor
    Serial.println(record);
    
    // Log to SD card
    if (sdAvailable) {
      File dataFile = SD.open("/data.csv", FILE_APPEND);
      if (dataFile) {
        dataFile.println(record);
        dataFile.close();
      } else {
        sdAvailable = false;
        Serial.println("[ERROR] Failed to write to SD card");
      }
    }
    
    // Increment sequence
    sequence++;
    
    // Status message every 10 samples
    if (sequence % 10 == 0) {
      Serial.println("----------------------------------------------------------------");
      Serial.printf("[INFO] %d samples acquired | Sensor: %s | Storage: %s\n",
                    sequence,
                    sensorOK ? "OK" : "ERROR",
                    sdAvailable ? "OK" : "ERROR");
      Serial.println("----------------------------------------------------------------");
    }
  }
  
  delay(10); // Small delay for stability
}

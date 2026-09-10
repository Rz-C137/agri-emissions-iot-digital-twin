#include "DHTesp.h"

DHTesp dht;

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("=== Agricultural IoT Monitoring System ===");
  Serial.println("Virtual Hardware Demo for ATB Interview");
  Serial.println("==========================================");
  
  dht.setup(4, DHTesp::DHT22);
  
  Serial.println("\n[OK] System initialized");
  Serial.println("\nSampling every 5 seconds...\n");
  Serial.println("Time,Sequence,Temp(C),Humidity(%),Status");
  Serial.println("------------------------------------------");
}

int sequence = 0;

void loop() {
  delay(5000);
  
  float temp = dht.getTemperature();
  float humidity = dht.getHumidity();
  
  char buffer[100];
  unsigned long seconds = millis() / 1000;
  
  if (dht.getStatus() == 0) {
    sprintf(buffer, "%02lu:%02lu:%02lu,%d,%.1f,%.1f,OK", 
            seconds/3600, (seconds/60)%60, seconds%60,
            sequence, temp, humidity);
  } else {
    sprintf(buffer, "%02lu:%02lu:%02lu,%d,ERROR,ERROR,SENSOR_FAIL",
            seconds/3600, (seconds/60)%60, seconds%60, sequence);
  }
  
  Serial.println(buffer);
  
  sequence++;
  
  if (sequence % 10 == 0) {
    Serial.println("------------------------------------------");
    Serial.print("[INFO] ");
    Serial.print(sequence);
    Serial.println(" samples acquired");
    Serial.println("------------------------------------------");
  }
}

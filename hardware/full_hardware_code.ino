#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// === Pins ===
#define TRIG_PIN 5
#define ECHO_PIN 18
#define SOIL_PIN 34
#define DHTPIN 23
#define DHTTYPE DHT22

// === Tank Settings ===
const int tankHeight = 100; // cm

// === Soil Moisture Settings ===
const int dry_reading = 4095;   // dry value
const int wet_reading = 1560;   // wet value

// === WiFi Settings ===
const char* ssid = "Piyush's OnePlus";
const char* password = "PiyushLal";

// === Server URL ===
String serverName = "http://10.192.75.231:5000/update";

// === DHT Sensor ===
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);

  // Pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // ADC settings
  analogReadResolution(12);
  analogSetPinAttenuation(SOIL_PIN, ADC_11db);

  // Initialize DHT
  dht.begin();

  // Connect WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected!");
}

// ===== Read single ultrasonic water level =====
int readWaterLevelSingle() {
  long duration;
  float distance;

  // Trigger ultrasonic
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout
  if (duration == 0) {
    Serial.println("No echo detected!");
    return -1; // invalid reading
  }

  distance = (duration * 0.0343) / 2; // cm
  distance = constrain(distance, 0, tankHeight);

  float filledHeight = tankHeight - distance;
  int waterLevelPercent = round((filledHeight / tankHeight) * 100);
  waterLevelPercent = constrain(waterLevelPercent, 0, 100);

  return waterLevelPercent;
}

// ===== Read soil moisture =====
int readSoilMoisture() {
  int moisture = analogRead(SOIL_PIN);
  // Ensure wet = 100% and dry = 0%
  int moisturePercent = map(moisture, wet_reading, dry_reading, 100, 0);
  moisturePercent = constrain(moisturePercent, 0, 100);
  return moisturePercent;
}

// ===== Read DHT22 =====
bool readDHT(float &humidity, float &temperature) {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)) return false; // reading failed
  return true;
}

// ===== Send JSON data =====
void sendData(int waterLevel, int soilMoisture, float humidity, float temperature) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected");
    return;
  }

  HTTPClient http;
  http.begin(serverName);
  http.addHeader("Content-Type", "application/json");

  String requestBody = "{";
  requestBody += "\"water_level\":" + String(waterLevel) + ",";
  requestBody += "\"soil_moisture\":" + String(soilMoisture) + ",";
  requestBody += "\"humidity\":" + String(humidity) + ",";
  requestBody += "\"temperature\":" + String(temperature);
  requestBody += "}";

  int httpResponseCode = http.POST(requestBody);

  if (httpResponseCode > 0) {
    Serial.print("POST Response Code: ");
    Serial.println(httpResponseCode);
    Serial.println(http.getString());
  } else {
    Serial.print("Error sending POST: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void loop() {
  int waterLevel = readWaterLevelSingle();
  int soilMoisture = readSoilMoisture();
  float humidity = 0, temperature = 0;

  if (!readDHT(humidity, temperature)) {
    Serial.println("Failed to read DHT22!");
  }

  Serial.println("=== Sensor Readings ===");
  Serial.print("Water Level: "); Serial.print(waterLevel); Serial.println("%");
  Serial.print("Soil Moisture: "); Serial.print(soilMoisture); Serial.println("%");
  Serial.print("Humidity: "); Serial.print(humidity); Serial.println("%");
  Serial.print("Temperature: "); Serial.print(temperature); Serial.println("C");
  Serial.println("=======================");

  sendData(waterLevel, soilMoisture, humidity, temperature);

  delay(2000); // wait 2s before next reading
}

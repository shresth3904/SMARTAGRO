#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// === Pins ===
#define TRIG_PIN 5
#define ECHO_PIN 18
#define SOIL_PIN 34
#define DHTPIN 23
#define DHTTYPE DHT22
#define RELAY_PIN 13   // Relay control pin

// === Tank Settings ===
const int tankHeight = 100; // cm

// === Soil Moisture Settings ===
const int dry_reading = 4095;
const int wet_reading = 1560;

// === WiFi Settings ===
const char* ssid = "Piyush's OnePlus";
const char* password = "PiyushLal";

// === Server URLs ===
String serverUpdateURL = "http://10.221.178.231:5000/update";
String serverCommandURL = "http://10.221.178.231:5000/pump";

// === DHT Sensor ===
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // HIGH = OFF (for NO relay)

  analogReadResolution(12);
  analogSetPinAttenuation(SOIL_PIN, ADC_11db);

  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected!");
}

// ===== Sensor Functions =====
int readWaterLevelSingle() {
  long duration;
  float distance;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return -1;

  distance = (duration * 0.0343) / 2;
  distance = constrain(distance, 0, tankHeight);

  float filledHeight = tankHeight - distance;
  int waterLevelPercent = round((filledHeight / tankHeight) * 100);
  return constrain(waterLevelPercent, 0, 100);
}

int readSoilMoisture() {
  int moisture = analogRead(SOIL_PIN);
  int moisturePercent = map(moisture, wet_reading, dry_reading, 100, 0);
  return constrain(moisturePercent, 0, 100);
}

bool readDHT(float &humidity, float &temperature) {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)) return false;
  return true;
}

void sendData(int waterLevel, int soilMoisture, float humidity, float temperature) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(serverUpdateURL);
  http.addHeader("Content-Type", "application/json");

  String body = "{";
  body += "\"water_level\":" + String(waterLevel) + ",";
  body += "\"soil_moisture\":" + String(soilMoisture) + ",";
  body += "\"humidity\":" + String(humidity) + ",";
  body += "\"temperature\":" + String(temperature);
  body += "}";

  int code = http.POST(body);
  Serial.print("POST: "); Serial.println(code);
  http.end();
}

// ===== Get relay command from server =====
void checkPumpCommand() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(serverCommandURL);
  int httpResponseCode = http.GET();

  if (httpResponseCode == 200) {
    String payload = http.getString();
    payload.trim();
    Serial.print("Command: ");
    Serial.println(payload);

    if (payload == "1") {
      digitalWrite(RELAY_PIN, LOW);  // Turn pump ON
      Serial.println("Pump: ON");
    } else if (payload == "0") {
      digitalWrite(RELAY_PIN, HIGH); // Turn pump OFF
      Serial.println("Pump: OFF");
    } else {
      Serial.println("Invalid command from server");
    }
  } else {
    Serial.print("Command fetch error: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void loop() {
  int waterLevel = readWaterLevelSingle();
  int soilMoisture = readSoilMoisture();
  float humidity = 0, temperature = 0;

  readDHT(humidity, temperature);

  Serial.println("=== Sensor Readings ===");
  Serial.printf("Water: %d%% | Soil: %d%% | Hum: %.1f%% | Temp: %.1f°C\n",
                waterLevel, soilMoisture, humidity, temperature);

  sendData(waterLevel, soilMoisture, humidity, temperature);
  checkPumpCommand();

  delay(200);
}


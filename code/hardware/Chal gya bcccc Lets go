#include <WiFi.h>
#include <WiFiManager.h>      // https://github.com/tzapu/WiFiManager
#include <HTTPClient.h>
#include <DHT.h>
#include <Preferences.h>      // ESP32 NVS storage
#include "esp_system.h"
#include "esp_mac.h"

// === Pins ===
#define TRIG_PIN 5
#define ECHO_PIN 18
#define SOIL_PIN_1 34
#define SOIL_PIN_2 35
#define DHTPIN 23
#define DHTTYPE DHT22
#define RELAY_PIN 13

// === Tank & Soil Settings ===
const int tankHeight = 100;   // cm
const int dry_reading = 4095;
const int wet_reading = 1560;

// === Globals ===
DHT dht(DHTPIN, DHTTYPE);
Preferences prefs;
bool shouldSaveConfig = false;
String serverBase = "";     // e.g. "http://192.168.1.100:5000"
String deviceID = "";

// === Callbacks ===
void saveConfigCallback() {
  shouldSaveConfig = true;
}

// === Build URLs ===
String updateURL()  { return serverBase + "/update"; }
String commandURL() { return serverBase + "/pump"; }

// === Device ID (MAC) ===
String getDeviceID() {
  if (deviceID != "") return deviceID;
  uint8_t mac[6];
  esp_efuse_mac_get_default(mac);
  char idStr[13];
  sprintf(idStr, "%02X%02X%02X%02X%02X%02X",
          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  deviceID = String(idStr);
  return deviceID;
}

int device_id=1;

void safeDelayMs(unsigned long ms) {
  // avoid very long blocking delays in case WiFi/HTTP needs background time
  unsigned long start = millis();
  while (millis() - start < ms) {
    yield(); // let ESP background tasks run
  }
}

void setup() {
  Serial.begin(115200);
  safeDelayMs(200);

  // Pin setup
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // default OFF for active-low relay boards

  analogReadResolution(12);
  analogSetPinAttenuation(SOIL_PIN_1, ADC_11db);
  analogSetPinAttenuation(SOIL_PIN_2, ADC_11db);

  dht.begin();

  // Load saved server
  prefs.begin("smartagro", false);
  String storedServer = prefs.getString("server", "");
  if (storedServer.length() == 0) {
    // fallback default (change to your dev server IP)
    storedServer = "http://10.76.158.59:5000";
  }
  serverBase = storedServer;

  // WiFiManager portal - NOTE: serverParam is a stack variable (NOT new) to avoid dangling pointers
  WiFi.mode(WIFI_STA);
  WiFiManager wifiManager;
  WiFiManagerParameter serverParam("server", "Server URL", serverBase.c_str(), 128);
  wifiManager.addParameter(&serverParam);
  wifiManager.setSaveConfigCallback(saveConfigCallback);

  Serial.println("Starting WiFiManager...");
  if (!wifiManager.autoConnect("SmartAgro-Setup")) {
    Serial.println("Failed to connect. Restarting...");
    safeDelayMs(3000);
    ESP.restart();
  }

  Serial.print("Connected to WiFi: ");
  Serial.println(WiFi.SSID());
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // IMPORTANT: copy the parameter value IMMEDIATELY while serverParam is still valid (stack)
  const char *val = serverParam.getValue();
  if (val != nullptr && strlen(val) > 0) {
    String newServer = String(val);
    if (shouldSaveConfig) {
      prefs.putString("server", newServer);
      Serial.println("Saved new server URL: " + newServer);
    }
    serverBase = newServer;
  } else {
    // If param empty, keep previously loaded serverBase (from prefs or default)
    Serial.println("Using stored/default server URL: " + serverBase);
  }
}

// === Sensors ===
int readWaterLevelSingle() {
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return -1;

  float distance = (duration * 0.0343) / 2.0;
  distance = constrain(distance, 0, tankHeight);
  float filledHeight = tankHeight - distance;
  int percent = round((filledHeight / tankHeight) * 100);
  return constrain(percent, 0, 100);
}

int readSoilMoisture(int pin) {
  int raw = analogRead(pin);
  int percent = map(raw, wet_reading, dry_reading, 100, 0);
  return constrain(percent, 100, 0);
}

bool readDHT(float &h, float &t) {
  h = dht.readHumidity();
  t = dht.readTemperature();
  return !(isnan(h) || isnan(t));
}

// === Communication ===
void sendData(int water, int soil, float hum, float temp) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected, skipping sendData()");
    return;
  }

  HTTPClient http;
  String url = updateURL();
  if (url.length() == 0) {
    Serial.println("No server URL configured, skipping POST");
    return;
  }

  // Use c_str() to avoid temporary String lifetime issues
  http.begin(url.c_str());
  http.addHeader("Content-Type", "application/json");

  String body = "{";
  body += "\"device_id\":\"" + String(device_id) + "\",";
  body += "\"water_level\":" + String(water) + ",";
  body += "\"soil_moisture\":" + String(soil) + ",";
  body += "\"humidity\":" + String(hum) + ",";
  body += "\"temperature\":" + String(temp);
  body += "}";

  int code = http.POST(body);
  Serial.print("POST: "); Serial.println(code);
  http.end();
}

void checkPumpCommand() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected, skipping checkPumpCommand()");
    return;
  }

  String url = commandURL() + "?device_id=" + String(device_id);
  if (serverBase.length() == 0) {
    Serial.println("No server URL configured, skipping GET");
    return;
  }

  HTTPClient http;
  http.begin(url.c_str());
  int httpResponseCode = http.GET();

  if (httpResponseCode == 200) {
    String payload = http.getString();
    payload.trim();
    Serial.print("Command: ");
    Serial.println(payload);

    if (payload == "1") {
      digitalWrite(RELAY_PIN, LOW);  // ON (active-low)
      Serial.println("Pump: ON");
    } else if (payload == "0") {
      digitalWrite(RELAY_PIN, HIGH); // OFF
      Serial.println("Pump: OFF");
    } else {
      Serial.println("Unknown pump payload");
    }
  } else {
    Serial.print("Command fetch error: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

void loop() {
  int waterLevel = readWaterLevelSingle();
  int soil1 = readSoilMoisture(SOIL_PIN_1);
  int soil2 = readSoilMoisture(SOIL_PIN_2);
  int avgSoil = (soil1 + soil2) / 2;

  float humidity = 0, temperature = 0;
  readDHT(humidity, temperature);

  Serial.println("=== Sensor Readings ===");
  Serial.printf("Device: %s | Water: %d%% | Soil1: %d%% | Soil2: %d%% | Avg Soil: %d%% | Hum: %.1f%% | Temp: %.1f°C\n",
                getDeviceID().c_str(), waterLevel, soil1, soil2, avgSoil, humidity, temperature);

  sendData(waterLevel, avgSoil, humidity, temperature);
  checkPumpCommand();

  safeDelayMs(2000);
}

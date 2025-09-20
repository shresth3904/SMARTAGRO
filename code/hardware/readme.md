# SmartAgro - ESP32 Firmware

This directory contains the Arduino C++ firmware for the ESP32 microcontroller, which serves as the core of the SmartAgro IoT device. This code is responsible for reading data from various environmental sensors, sending it to a central server, and receiving commands to control the irrigation pump.

## Circuit Diagram
![Circuit Diagram](./code/hardware/circuit_diagram.png)

## Features ✨

* **Dynamic WiFi Configuration:** Uses the **WiFiManager** library to create a configuration portal on first boot. This allows you to set up WiFi credentials and the server URL without hardcoding them.
* **Persistent Configuration:** Saves the server URL to the ESP32's non-volatile storage, so it only needs to be configured once.
* **Multi-Sensor Data Collection:** Reads data from:
    * Two Capacitive Soil Moisture Sensors
    * DHT22 Temperature & Humidity Sensor
    * HC-SR04 Ultrasonic Sensor for water tank level
* **Remote Actuator Control:** Fetches commands from the server to turn a water pump ON or OFF via a relay module.
* **Robust Communication:** Uses HTTP POST requests to send sensor data in JSON format and HTTP GET requests to poll for commands.

## Hardware Requirements 🛠️

To build the hardware for this project, you will need the following components:

* **Microcontroller:** ESP32 Dev Kit C (or a similar ESP32 board)
* **Sensors:**
    * 2 x Capacitive Soil Moisture Sensor
    * 1 x DHT22 (or DHT11) Temperature and Humidity Sensor
    * 1 x HC-SR04 Ultrasonic Distance Sensor
* **Actuator:**
    * 1 x 5V Single Channel Relay Module
    * 1 x Submersible Water Pump (with its own power supply)
* **Miscellaneous:** Breadboard, jumper wires, and a power supply for the ESP32.

## Pinout Configuration 📌

The firmware is configured with the following pin connections. You must wire your components to these specific GPIO pins on the ESP32.

| Component                 | ESP32 Pin |
| ------------------------- | :-------: |
| Ultrasonic Sensor TRIG    |    `5`    |
| Ultrasonic Sensor ECHO    |    `18`   |
| Soil Moisture Sensor 1    |    `34`   |
| Soil Moisture Sensor 2    |    `35`   |
| DHT22 Sensor Data         |    `23`   |
| Relay Module IN           |    `13`   |

## Library Dependencies 📚

This project relies on several external libraries. You can install them through the Arduino IDE's Library Manager (`Sketch > Include Library > Manage Libraries...`):

* `WiFiManager` by tzapu
* `DHT sensor library` by Adafruit
* `Adafruit Unified Sensor` by Adafruit

The `WiFi.h`, `HTTPClient.h`, and `Preferences.h` libraries are included with the ESP32 board package and do not require separate installation.

## Setup and Installation ⚙️

1.  **Arduino IDE Setup:**
    * Make sure you have the ESP32 board definitions installed in your Arduino IDE. If not, follow the instructions on the [official Espressif documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
    * Install all the libraries listed in the **Library Dependencies** section.
    * Select your ESP32 board from the `Tools > Board` menu (e.g., "ESP32 Dev Module").
    * Select the correct COM port from the `Tools > Port` menu.

2.  **Sensor Calibration:**
    * Before uploading, you may need to calibrate the soil moisture sensors. In the code, adjust the `dry_reading` and `wet_reading` values based on readings you take when the sensor is completely dry vs. submerged in water.
    * Update the `tankHeight` constant to match the height of your water tank in centimeters for accurate level readings.

3.  **Upload the Code:**
    * Open the `.ino` file in the Arduino IDE and click the "Upload" button.

4.  **First-Time Configuration (WiFiManager):**
    * When the ESP32 boots for the first time, it will fail to connect to a known network and will create its own Wi-Fi Access Point.
    * On your phone or computer, connect to the Wi-Fi network named **"SmartAgro-Setup"**.
    * A captive portal should automatically open in your browser. If it doesn't, navigate to `192.168.4.1`.
    * On the portal page:
        1.  Click **"Configure WiFi"**.
        2.  Select your home/farm Wi-Fi network from the list.
        3.  Enter your Wi-Fi password.
        4.  In the **"Server URL"** field, enter the full URL of your backend server (e.g., `http://192.168.1.10:5000`).
        5.  Click **"Save"**.
    * The ESP32 will then save these settings, restart, and attempt to connect to your network and server. You only need to do this once.

## How It Works 🧠

### `setup()`
* Initializes serial communication for debugging.
* Sets the pin modes for all connected sensors and the relay.
* Loads the previously saved server URL from non-volatile `Preferences`.
* Starts the WiFiManager. If credentials are not saved, it launches the configuration portal. Otherwise, it connects to the saved Wi-Fi network.
* After connecting, it updates the `serverBase` variable with the URL provided through the portal.

### `loop()`
The main loop runs continuously to perform the core functions of the device:
1.  **Read Sensors:** It calls functions to read the water level, the values from both soil moisture sensors, and the temperature/humidity. It then calculates the average soil moisture.
2.  **Log to Serial:** Prints all the collected sensor data to the Serial Monitor for live debugging.
3.  **Send Data:** It packages the sensor readings into a JSON object and sends them to the `/update` endpoint on the server via an HTTP POST request.
4.  **Fetch Command:** It sends an HTTP GET request to the `/pump` endpoint to check for a new command (`0` for OFF, `1` for ON).
5.  **Control Pump:** Based on the received command, it sets the relay pin to `HIGH` (OFF) or `LOW` (ON).
6.  **Delay:** Waits for a few seconds before repeating the cycle.

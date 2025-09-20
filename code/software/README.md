# SmartAgro: Smart Irrigation for Hilly Regions

SmartAgro is an IoT-based smart irrigation system designed to address the challenges of water scarcity and inefficient farming in hilly regions like Jorethang, South Sikkim. By integrating real-time sensor data, weather forecasts, and crop-specific intelligence, it automates the irrigation process to conserve water, enhance crop yields, and reduce manual labor for farmers.



## Tasks Accomplished

✅ **Task 1:** Developed a full-stack IoT solution, including hardware integration, a backend server, and a frontend user dashboard.<br>
✅ **Task 2:** Implemented a multi-conditional `AUTO` mode that considers soil moisture, crop type, weather forecasts, and water tank levels.<br>
✅ **Task 3:** Created a secure authentication system allowing users to register and link their specific hardware device for personalized monitoring and notifications.<br>

***

## Technology Stack

This project leverages the following technologies:

* **Python & Flask:** Chosen for its simplicity and robustness in building the backend REST APIs and handling core application logic.
* **Flask-Login:** Used to manage user sessions for secure authentication, handling logging in, logging out, and remembering users.
* **Werkzeug:** Provides essential utilities for WSGI applications, used here for securely handling passwords by generating and checking hashes.
* **SQLite3:** A lightweight, serverless database used for managing user accounts, device registrations, and sensor data logs efficiently.
* **HTML/CSS/JS:** Used to create a responsive, intuitive, and interactive frontend dashboard for data visualization and user control.
* **Chart.js:** A powerful JavaScript library used to render historical sensor data into interactive and easy-to-understand charts.
* **WeatherAPI.com:** Integrated to fetch real-time weather forecasts, enabling the system to make smarter, weather-aware irrigation decisions.
* **Telegram Bot API:** Used to push instant, real-time notifications to users about the system's status and critical alerts.
* **ESP32 Microcontroller:** The core of the hardware system, chosen for its built-in Wi-Fi capabilities and performance in reading sensor data and controlling the pump.

***

## Key Features

* **Multi-Conditional AUTO Mode:** The intelligent `AUTO` mode uses a logic engine that makes decisions based on four key factors: current **soil moisture**, the selected **crop's needs**, real-time **weather forecasts** (disabling irrigation if rain is likely), and available **water tank level**.
* **Secure User & Device Management:** Features a robust user authentication system and a one-time device registration process, ensuring that each user can only access the personalized dashboard and data from their own hardware.
* **Dual Operation & Scheduling:** Allows users to switch seamlessly between the intelligent `AUTO` mode and a direct `MANUAL` override. Users can also set specific time windows to define when the system is permitted to operate.
* **Real-time Monitoring and Alerts:** The dashboard displays live sensor data on interactive charts and gauges, while the system pushes instant Telegram notifications for critical events like low water levels or pump activation.

***

## Local Setup Instructions (Write for both windows and macos)

Follow these steps to run the project locally.

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/shresth3904/SMARTAGRO.git](https://github.com/shresth3904/SMARTAGRO.git)
    cd SMARTAGRO/code/software
    ```

2.  **Create and Activate a Virtual Environment**
    * **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Required Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Keys and Secret Key**

    Open the `app.py` file and replace the placeholder values with your actual keys:

    ```python
    # Line 19
    app.config['SECRET_KEY'] = 'your_strong_secret_key'

    # Line 21
    TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    # Line 301
    API_KEY = 'YOUR_WEATHERAPI_COM_KEY'
    ```

5.  **Run the Flask Application**
    ```bash
    flask run
    ```
    The application will now be running and accessible at **http://127.0.0.1:5000**.

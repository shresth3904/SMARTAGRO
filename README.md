# SmartAgro: Smart Irrigation for Hilly Regions

### PS Chosen: Implementation of Smart Agriculture for Efficient Cultivation in Hilly Regions (ID: 25062)

The project directly addresses the problem statement **"Implementation of Smart Agriculture for Efficient Cultivation in Hilly Regions"** by providing an affordable, automated irrigation solution tailored to conserve water and improve crop yields in water-scarce areas like Jorethang, South Sikkim.

---

## Team Details

**Team Name:** SmartAgro
* **Team Leader:** Piyush Lal - [@piyushlal2005](https://github.com/piyushlal2005)<br><br>
 **Team Members:**<br>
* **Shresth** - [@shresth3904](https://github.com/shresth3904)
* **Daksh Gulia** - [@DakshGulia475](https://github.com/DakshGulia475)
* **Tanay Agarwal** - [@tanayagarwal-2006](https://github.com/tanayagarwal-2006)
* **Vedika Choudhary** - [@vedikachoudhary20](https://github.com/vedikachoudhary20)
* **Pratham Sagar** - [@oscillocode](https://github.com/oscillocode)


---

## 🔗 Project Links

* **SIH Presentation:** [Final SIH Presentation](https://github.com/your-username/your-repo/blob/main/SIH_Presentation.pptx)
* **Video Demonstration:** [Watch Video](https://www.youtube.com/watch?v=your_unlisted_video_id)
* **Source Code:** [GitHub Repository](https://github.com/shresth3904/SMARTAGRO)
* **Live Deployment** [SmartAgro](https://smartagro.pythonanywhere.com/)

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Flask-Login
* **Database:** SQLite3
* **Frontend:** HTML, CSS, JavaScript
* **Data Visualization:** Chart.js
* **External APIs:**
    * WeatherAPI.com (for real-time weather forecasts)
    * Telegram Bot API (for notifications)
* **Hardware (Conceptual):** ESP32, Soil Moisture Sensor, DHT11 (Temperature & Humidity), Ultrasonic Sensor (Water Level).

---

## ✨ Key Features

### User & System Management
* **User Authentication:** Secure user registration and login functionality.
* **Device Registration:** A one-time setup process to link a user account with a unique hardware device ID and code.
* **Personalized Dashboard:** Each user has a dedicated dashboard displaying data only from their registered device.

### Intelligent Irrigation Control
* **Dual Operation Modes:**
    * **AUTO Mode:** A fully automated, intelligent logic that controls the pump based on multiple factors.
    * **MANUAL Mode:** Allows the user to toggle the pump ON/OFF directly from the dashboard.
* **Crop Intelligence:** Irrigation thresholds are dynamically set based on the selected crop and its current growth stage from a pre-defined database schedule.
* **Weather Integration:** The system fetches real-time weather data. In AUTO mode, it automatically disables irrigation if there is a high probability of rain, conserving water.
* **Resource Management:** Monitors the water tank level and prevents the pump from running dry, protecting the hardware.
* **Time-Based Scheduling:** Users can define specific time windows (e.g., 06:00 to 18:00) during which the irrigation system is permitted to operate.

### Monitoring & Visualization
* **Real-time Sensor Data:** The dashboard displays live data for soil moisture, ambient temperature, humidity, and water tank level.
* **Interactive Charts:** Historical data for each sensor is plotted on graphs to visualize trends over time.
* **Intuitive UI:** Custom-designed UI elements like gauges, bars, and thermometers provide an at-a-glance understanding of the current farm conditions.
* **System Notifications:** The system sends critical alerts and status updates (e.g., "Pump ON," "Water level low") to the user's Telegram.

---

## 🚀 How to Run Locally

Follow these steps to set up and run the project on your local machine.

### Prerequisites
* Python 3.8+
* `pip` (Python package installer)

### Installation & Setup

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/shresth3904/SMARTAGRO.git](https://github.com/shresth3904/SMARTAGRO.git)
    cd SMARTAGRO/code/software
    ```

2.  **Create and Activate a Virtual Environment**
    * On macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set Up API Keys**
    In the `app.py` file, replace the placeholder values for the following variables with your actual keys:
    ```python
    # Line 19
    app.config['SECRET_KEY'] = 'your_strong_secret_key'

    # Line 21
    TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    # Line 301
    API_KEY = 'YOUR_WEATHERAPI_COM_KEY'
    ```
    

5.  **Run the Application**
    ```sh
    flask run
    ```
    Alternatively, you can run the Python script directly:
    ```sh
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000`.

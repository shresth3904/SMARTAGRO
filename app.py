from flask import Flask, request, render_template, redirect, url_for, jsonify, request
import sqlite3, random
import requests
import time, threading

app = Flask(__name__)

weather_cond = False

category_ids = {
    "Clear / Fair Weather": 1,
    "Rain / Drizzle": 2,
    "Thunderstorms": 3,
    "Snow / Ice": 4,
    "Fog / Mist / Haze": 5,
    "Wind / Dust": 6,
    "Cloud Coverage": 7
}

weather_category = {
    1000: 1,
    1003: 7,
    1006: 7,
    1009: 7,
    1030: 5,
    1063: 2,
    1150: 2,
    1153: 2,
    1168: 2,
    1171: 2,
    1180: 2,
    1183: 2,
    1186: 2,
    1189: 2,
    1192: 2,
    1195: 2,
    1240: 2,
    1243: 2,
    1246: 2,
    1066: 4,
    1114: 4,
    1117: 4,
    1210: 4,
    1213: 4,
    1216: 4,
    1219: 4,
    1222: 4,
    1225: 4,
    1237: 4,
    1255: 4,
    1258: 4,
    1261: 4,
    1264: 4,
    1087: 3,
    1273: 3,
    1276: 3,
    1279: 3,
    1282: 3,
    1135: 5,
    1147: 5,
    1069: 4,
    1072: 2,
    1198: 2,
    1201: 2,
    1204: 4,
    1207: 4,
    1249: 4,
    1252: 4
}


weather_logo = {
    1: """<div class="weather-card">
                <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Clear / Fair Weather</title>
                    <circle cx="32" cy="32" r="8" stroke="#FDB813" stroke-width="2.5"/>
                    <line x1="32" y1="16" x2="32" y2="20" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="32" y1="44" x2="32" y2="48" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="48" y1="32" x2="44" y2="32" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="20" y1="32" x2="16" y2="32" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="43.07" y1="20.93" x2="40.24" y2="23.76" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="23.76" y1="40.24" x2="20.93" y2="43.07" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="43.07" y1="43.07" x2="40.24" y2="40.24" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="23.76" y1="23.76" x2="20.93" y2="20.93" stroke="#FDB813" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
                
            </div>""",
    2:"""<div class="weather-card">
                <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Rain / Drizzle</title>
                    <path d="M47.9,35.3c3.3-0.2,6.1-2.9,6.1-6.3c0-3.5-2.8-6.4-6.3-6.4c-0.3,0-0.6,0-0.9,0.1 c-1.5-4.3-5.7-7.4-10.8-7.4c-5.5,0-10,4.5-10,10c0,0.8,0.1,1.5,0.3,2.2" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M26.3,27.2C22.5,27.9,19,31.4,19,35.7c0,4.6,3.7,8.3,8.3,8.3h20.3" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="28" y1="48" x2="26" y2="52" stroke="#87CEEB" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="36" y1="48" x2="34" y2="52" stroke="#87CEEB" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="44" y1="48" x2="42" y2="52" stroke="#87CEEB" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
    
            </div>""",
    3:"""<div class="weather-card">
                <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Thunderstorms</title>
                    <path d="M47.9,35.3c3.3-0.2,6.1-2.9,6.1-6.3c0-3.5-2.8-6.4-6.3-6.4c-0.3,0-0.6,0-0.9,0.1 c-1.5-4.3-5.7-7.4-10.8-7.4c-5.5,0-10,4.5-10,10c0,0.8,0.1,1.5,0.3,2.2" stroke="#778899" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M26.3,27.2C22.5,27.9,19,31.4,19,35.7c0,4.6,3.7,8.3,8.3,8.3h20.3" stroke="#778899" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <polyline points="38,44 32,50 36,50 30,58" stroke="#FFC107" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
      
            </div>""",
    4:"""<div class="weather-card">
                <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Snow / Ice</title>
                    <path d="M47.9,35.3c3.3-0.2,6.1-2.9,6.1-6.3c0-3.5-2.8-6.4-6.3-6.4c-0.3,0-0.6,0-0.9,0.1 c-1.5-4.3-5.7-7.4-10.8-7.4c-5.5,0-10,4.5-10,10c0,0.8,0.1,1.5,0.3,2.2" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M26.3,27.2C22.5,27.9,19,31.4,19,35.7c0,4.6,3.7,8.3,8.3,8.3h20.3" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M28 48 L 28 54 M 25 51 L 31 51 M 26 49 L 30 53 M 30 49 L 26 53" stroke="#ADD8E6" stroke-width="2.5" stroke-linecap="round"/>
                    <path d="M40 48 L 40 54 M 37 51 L 43 51 M 38 49 L 42 53 M 42 49 L 38 53" stroke="#ADD8E6" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
            
            </div>""",
    5:"""<div class="weather-card">
                <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Fog / Mist / Haze</title>
                    <path d="M16 28 C 22 24, 30 24, 36 28" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round"/>
                    <path d="M20 36 C 28 32, 38 32, 46 36" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round"/>
                    <path d="M14 44 C 24 40, 36 40, 48 44" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
            </div>""",
    6:"""<div class="weather-card">
                 <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Wind / Dust</title>
                    <path d="M16 32 C 24 26, 36 26, 46 32" stroke="#BDB76B" stroke-width="2.5" stroke-linecap="round" fill="none"/>
                    <path d="M12 42 C 22 36, 34 36, 48 42" stroke="#BDB76B" stroke-width="2.5" stroke-linecap="round" fill="none"/>
                    <circle cx="52" cy="31" r="1.5" fill="#BDB76B"/>
                    <circle cx="50" cy="45" r="1.5" fill="#BDB76B"/>
                    <circle cx="10" cy="35" r="1" fill="#BDB76B"/>
                </svg>
            </div>""",
    7:"""<div class="weather-card">
                <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <title>Cloud Coverage</title>
                    <path d="M47.9,43.3c3.3-0.2,6.1-2.9,6.1-6.3c0-3.5-2.8-6.4-6.3-6.4c-0.3,0-0.6,0-0.9,0.1 C45.3,26.4,41.1,23,36,23c-5.5,0-10,4.5-10,10c0,0.8,0.1,1.5,0.3,2.2" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M26.3,35.2C22.5,35.9,19,39.4,19,43.7c0,4.6,3.7,8.3,8.3,8.3h20.3" stroke="#B0C4DE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>"""
}

API_KEY = '91251ddd30ce4a8e862203910251009'  # Replace with your actual API key
CITY = 'delhi'

def send_msg(msg, chat_id):
    BOT_TOKEN = "8281251787:AAGEnx21qebtG0VS8h9gdckkUZ5bPLoYS6E"
    CHAT_ID = chat_id

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=1&aqi=no&alerts=no"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    city = f"{data['location']['name']}, {data['location']['country']}"
    temperature = f"{data['current']['temp_c']} °C"
    precipitation = f"{data['forecast']['forecastday'][0]['day']['totalprecip_mm']} mm"
    rain_chance = f"{data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']}%"
    condition = data['current']['condition']['text']
    cond_code = data['current']['condition']['code']
    weather = {'location':city, 'temp':temperature, 'prec':precipitation, 'prob':rain_chance, 'cond':condition, 'category':weather_category.get(cond_code, 1)}
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    mode_result = cur.execute("SELECT mode FROM system_mode WHERE id = 1").fetchone()
    current_mode = mode_result[0] if mode_result else 'AUTO'
    pump_status = cur.execute("SELECT command FROM pump_command ORDER BY id DESC LIMIT 1").fetchone()
    cur.execute("SELECT id, moisture FROM parameters ORDER BY id DESC LIMIT 10")
    moisture =  [['id', 'moisture']] + list(cur.fetchall())[::-1]
    temp = [['id', 'temp']] + list(cur.execute("SELECT id, temp FROM parameters ORDER BY id DESC LIMIT 10").fetchall())[::-1]
    humidity = [['id', 'humidity']] + list(cur.execute("SELECT id, humidity  FROM parameters ORDER BY id DESC LIMIT 10").fetchall())[::-1]
    water_lvl = [['id', 'water_lvl']] + list(cur.execute("SELECT id, water_lvl FROM parameters ORDER BY id DESC LIMIT 10").fetchall())[::-1]
    current_val = list(cur.execute("SELECT moisture, temp, humidity, water_lvl FROM parameters ORDER BY time DESC LIMIT 1").fetchone())
    cur.execute("SELECT DISTINCT crop_name, growth_stage FROM irrigation_schedule ORDER BY crop_name, id")
    all_schedules = cur.fetchall()
    crop_data = {}
    for crop, stage in all_schedules:
        if crop not in crop_data:
            crop_data[crop] = []
        if stage:
            crop_data[crop].append(stage)

    current_settings_result = cur.execute("SELECT crop_name, growth_stage FROM system_settings WHERE id = 1").fetchone()
    current_settings = {
        'crop_name': current_settings_result[0],
        'growth_stage': current_settings_result[1]
    }
    con.close()
    
    return render_template('dashboard.html',
                           data=moisture, 
                           temp = temp, 
                           humidity = humidity, 
                           water_lvl = water_lvl ,
                           current_val=current_val, 
                           weather = weather, 
                           weather_logo = weather_logo,
                           current_mode = current_mode,
                           pump_status = pump_status,
                           crop_data = crop_data,
                           current_settings = current_settings
                           )

@app.route('/update_settings', methods=['POST'])
def update_settings():

    selected_crop = request.form.get('crop_name')
    selected_stage = request.form.get('growth_stage')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    
    cur.execute("UPDATE system_settings SET crop_name = ?, growth_stage = ? WHERE id = 1", (selected_crop, selected_stage))
    conn.commit()
    conn.close()

    print(f"System settings updated to: {selected_crop} - {selected_stage}")

    return redirect(url_for('dashboard'))


@app.route('/about')
def about():
    return render_template('about.html')
def changeval():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    moisture = random.randrange(0, 100)
    temp = random.randrange(0, 100)
    humidity = random.randrange(0, 100)
    water_lvl = random.randrange(0, 100)
    cur.execute("INSERT INTO parameters(moisture, temp, humidity, water_lvl) VALUES (?, ?, ?, ?)", (moisture, temp, humidity, water_lvl))
    conn.commit()
    conn.close()
    print("SAVED :",(moisture, temp, humidity, water_lvl))




@app.route('/weather')
def get_weather():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=1&aqi=no&alerts=no"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        city = f"{data['location']['name']}, {data['location']['country']}"
        temperature = f"{data['current']['temp_c']} °C"
        precipitation = f"{data['forecast']['forecastday'][0]['day']['totalprecip_mm']} mm"
        rain_chance = f"{data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']}%"
        condition = data['current']['condition']['text']
        print(city, temperature, precipitation, rain_chance, condition)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Weather in {city}</title>
            <style>
                body {{
                    background-color: #121212;
                    color: #ccc;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .weather_card {{
                    background-color: #1e1e1e;
                    border: 1px solid #555;
                    border-radius: 15px;
                    padding: 20px 30px;
                    width: 300px;
                    text-align: center;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                }}
                .weather_card h2 {{
                    margin-bottom: 10px;
                }}
                .weather_card p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="weather_card">
                <h2>Weather in {city}</h2>
                <p><strong>Condition:</strong> {condition}</p>
                <p><strong>Condition:</strong> {weather_category[condition]}</p>
                <p><strong>Temperature:</strong> {temperature}</p>
                <p><strong>Precipitation:</strong> {precipitation}</p>
                <p><strong>Chance of Rain:</strong> {rain_chance}</p>
            </div>
        </body>
        </html>
        """
        
        return html_content

    except requests.RequestException as e:
        return f"<h2>Error fetching weather data</h2><p>{str(e)}</p>"
@app.route('/update', methods = ['POST', 'GET']) 
def get_data():
    data = request.get_json()
    print("received", data)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    moisture = data['soil_moisture']
    temp = data['temperature']
    humidity = data['humidity']
    water_lvl = data['water_level']
    cur.execute("INSERT INTO parameters(moisture, temp, humidity, water_lvl) VALUES (?, ?, ?, ?)", (moisture, temp, humidity, water_lvl))
    conn.commit()
    conn.close()
    print("SAVED :",(moisture, temp, humidity, water_lvl))
    return jsonify({'status':'success', 'recieved':data}), 200

@app.route('/pump', methods = ['GET', 'POST'])
def pump():
    if (request.method == 'GET'):
        status = request.get_json()['status']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        
        status = cur.execute("SELECT command FROM pump_command ORDER BY id DESC LIMIT 1").fetchone()[0]
        cur.execute("INSERT INTO pump_connection(status) VALUES (?)", (status,))
        conn.commit()
        conn.close()
        print(status)
        return str(status)
    elif (request.method == 'POST'):
        status = request.get_json()['status']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO pump_command(command) VALUES (?)", (status,))
        conn.commit()
        conn.close()

@app.route('/pump_status', methods = ['GET'])
def pump_status():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    status = cur.execute("SELECT id, status FROM pump_connection ORDER BY id DESC LIMIT 1").fetchone()
    command = cur.execute("SELECT command FROM pump_command ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return jsonify(status, command)
    

@app.route('/fetch_parameters')
def fetch_parameters():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT id , moisture, temp, humidity, water_lvl FROM parameters ORDER BY id DESC LIMIT 10")
    data = cur.fetchall()
    changeval()
    return jsonify(data)


@app.route('/set_mode', methods=['POST'])
def set_mode():
    data = request.get_json()
    new_mode = data.get('mode')
    if new_mode in ['AUTO', 'MANUAL']:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("UPDATE system_mode SET mode = ? WHERE id = 1", (new_mode,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'mode': new_mode})
    return jsonify({'status': 'error', 'message': 'Invalid mode'}), 400

@app.route('/toggle_pump', methods=['POST'])
def toggle_pump():
    data = request.get_json()
    command = data.get('command')
    if command in [0, 1]:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO pump_command (command) VALUES (?)", (command,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'command': command})
    return jsonify({'status': 'error', 'message': 'Invalid command'}), 400




def auto_mode_logic():
    
    SATURATION_POINT = 95    
    RAIN_CHANCE_THRESHOLD = 70 
    RAIN_AMOUNT_THRESHOLD = 10
    WATER_TANK_MIN_LEVEL = 20  
    
   
    PERMITTED_START_HOUR = 4   
    PERMITTED_END_HOUR = 10   
    while True:
        time.sleep(5)
        
        conn = None
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            mode_result = cur.execute("SELECT mode FROM system_mode WHERE id = 1").fetchone()
            current_mode = mode_result[0] if mode_result else 'AUTO'
            print(current_mode)
            if current_mode != 'AUTO':
                conn.close()
                continue

            settings_result = cur.execute("SELECT crop_name, growth_stage FROM system_settings WHERE id = 1").fetchone()
            if not settings_result:
                print("[AUTO MODE] Error: Crop settings not found.")
                conn.close()
                continue
            crop_name, growth_stage = settings_result
            print(crop_name, growth_stage)
            threshold_result = cur.execute(
                "SELECT start_irrigation_threshold_fc FROM irrigation_schedule WHERE crop_name = ? AND growth_stage = ?",
                (crop_name, growth_stage)
            ).fetchone()
            if not threshold_result:
                print(f"[AUTO MODE] Error: No schedule found for {crop_name} ({growth_stage}).")
                conn.close()
                continue
            start_threshold = threshold_result[0]
            print(start_threshold)
            sensor_result = cur.execute("SELECT moisture, water_lvl FROM parameters ORDER BY id DESC LIMIT 1").fetchone()
            if not sensor_result:
                conn.close()
                continue
            latest_moisture, water_level = sensor_result
            print("latest_moisture, water_level", latest_moisture, water_level)
            url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=1&aqi=no&alerts=no"
            response = requests.get(url)
            weather_data = response.json()
            rain_chance = weather_data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
            precip_mm = weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm']
            print("rain_chance, precip_mm", rain_chance, precip_mm)
            current_hour = time.localtime().tm_hour
            last_command_result = cur.execute("SELECT command FROM pump_command ORDER BY id DESC LIMIT 1").fetchone()
            last_command = last_command_result[0] if last_command_result else 0
            print("last_command", last_command)
            new_command = None
            reason = ""

    
            if rain_chance > RAIN_CHANCE_THRESHOLD or precip_mm > RAIN_AMOUNT_THRESHOLD:
                new_command = 0
                reason = f"Pump OFF for {crop_name}. Skipping due to rain forecast in {CITY} ({rain_chance}% chance)."
            
            elif water_level < WATER_TANK_MIN_LEVEL:
                new_command = 0
                reason = f"Pump OFF. CRITICAL: Water tank level is low ({water_level}%)."

            elif latest_moisture > SATURATION_POINT:
                new_command = 0
                reason = f"Pump OFF for {crop_name}. Soil moisture ({latest_moisture}%) is above saturation point."
            
            elif not (PERMITTED_START_HOUR <= current_hour < PERMITTED_END_HOUR):
                new_command = 0
                reason = f"Command override: Current hour ({current_hour}) is outside the permitted schedule ({PERMITTED_START_HOUR}:00 - {PERMITTED_END_HOUR}:00)."
            
            elif latest_moisture < start_threshold and (PERMITTED_START_HOUR <= current_hour < PERMITTED_END_HOUR):
                new_command = 1
                reason = f"Pump ON for {crop_name} ({growth_stage}). Moisture ({latest_moisture}%) is below threshold ({start_threshold}%)."

            if new_command is not None and new_command != last_command:
                cur.execute("INSERT INTO pump_command (command) VALUES (?)", (new_command,))
                conn.commit()
                if reason: 
                    print(f"[AUTO MODE] {reason}")
                    send_msg(reason, "1234815808")

        except Exception as e:
            print(f"Error in auto_mode_logic thread: {e}")
        
        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    auto_thread = threading.Thread(target=auto_mode_logic, daemon=True)
    auto_thread.start()
    app.run(host = "0.0.0.0", port = 5000, debug = True, use_reloader=False)
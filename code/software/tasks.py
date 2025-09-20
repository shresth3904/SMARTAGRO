import sqlite3
import requests
import time
from datetime import datetime



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
        
        
SATURATION_POINT = 95
RAIN_CHANCE_THRESHOLD = 70
RAIN_AMOUNT_THRESHOLD = 10
WATER_TANK_MIN_LEVEL = 20

def auto_mode_logic():
        conn = None
        try:
            conn = sqlite3.connect('database.db', timeout=10)
            cur = conn.cursor()

            device_ids_result = cur.execute("SELECT DISTINCT device_id FROM system_settings").fetchall()
            if not device_ids_result:
                return
            
            for device_tuple in device_ids_result:
                print(device_tuple)
                device_id = device_tuple[0]
                
                try:
                    mode_result = cur.execute(
                        "SELECT mode FROM system_mode WHERE device_id = ?",
                        (device_id,)
                    ).fetchone()
                    
                    current_mode = mode_result[0] if mode_result else 'MANUAL'
                    
                    if current_mode != 'AUTO':
                        return
                    
                    settings_result = cur.execute(
                        "SELECT crop_name, growth_stage, city, start_at, end_at FROM system_settings WHERE device_id = ?",
                        (device_id,)
                    ).fetchone()
                    
                    print(settings_result)

                    if not settings_result:
                        print(f"[Device {device_id}] Error: System settings not found. Skipping.")
                        return
                    crop_name, growth_stage, city, start_time_str, end_time_str = settings_result
                    print(crop_name, growth_stage, city, start_time_str, end_time_str)
                    threshold_result = cur.execute(
                        "SELECT start_irrigation_threshold_fc FROM irrigation_schedule WHERE crop_name = ? AND growth_stage = ?",
                        (crop_name, growth_stage)
                    ).fetchone()

                    if not threshold_result:
                        print(f"[Device {device_id}] Error: No schedule for {crop_name} ({growth_stage}). Skipping.")
                        return
                    start_threshold = threshold_result[0]

                    sensor_result = cur.execute(
                        "SELECT moisture, water_lvl FROM parameters WHERE device_id = ? ORDER BY id DESC LIMIT 1",
                        (device_id,)
                    ).fetchone()
                    
                    print(sensor_result)
                    if not sensor_result:
                        print(f"[Device {device_id}] Error: No sensor data found. Skipping.")
                        return
                    latest_moisture, water_level = sensor_result

                    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"
                    response = requests.get(url)
                    response.raise_for_status()
                    weather_data = response.json()
                    rain_chance = weather_data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
                    precip_mm = weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm']

                    last_command_result = cur.execute(
                        "SELECT command FROM pump_command WHERE device_id = ? ORDER BY id DESC LIMIT 1",
                        (device_id,)
                    ).fetchone()
                    last_command = last_command_result[0] if last_command_result else 0

                    current_time_obj = datetime.now().time()
                    start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
                    end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()
                    
                    new_command = None
                    reason = ""

                    if rain_chance > RAIN_CHANCE_THRESHOLD or precip_mm > RAIN_AMOUNT_THRESHOLD:
                        new_command = 0
                        reason = f"Pump OFF. High rain forecast in {city} ({rain_chance}% chance)."
                    elif water_level < WATER_TANK_MIN_LEVEL:
                        new_command = 0
                        reason = f"Pump OFF. CRITICAL: Water tank level low ({water_level}%)."
                    elif latest_moisture > SATURATION_POINT:
                        new_command = 0
                        reason = f"Pump OFF. Soil moisture ({latest_moisture}%) is above saturation."
                    elif not (start_time_obj <= current_time_obj < end_time_obj):
                        new_command = 0
                        reason = f"Pump OFF. Outside of permitted schedule ({start_time_str} - {end_time_str})."
                    elif latest_moisture < start_threshold:
                        new_command = 1
                        reason = f"Pump ON for {crop_name}. Moisture ({latest_moisture}%) is below threshold ({start_threshold}%)."
                    else:
                        new_command = 0
                        reason = f"Pump OFF. Moisture ({latest_moisture}%) is sufficient."
                    print(reason, device_tuple)
                    if new_command is not None and new_command != last_command:
                        cur.execute("INSERT INTO pump_command (device_id, command) VALUES (?, ?)", (device_id, new_command))
                        
                        if reason:
                            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                            msg = f"[Device {device_id} | AUTO MODE] {reason}"
                            cur.execute("INSERT INTO notifications (device_id, msg, time) VALUES (?, ?, ?)", (device_id, msg, now_str))
                            send_msg(f"{msg}\n\n{now_str}", "1234815808")
                        
                        conn.commit()
                        print(f"[Device {device_id}] Action: {reason}")

                except requests.RequestException as e:
                    print(f"[Device {device_id}] Weather API Error: {e}")
                except Exception as e:
                    print(f"[Device {device_id}] Error in processing loop: {e}")
        
        except Exception as e:
            print(f"[AUTO MODE] Critical error in main thread: {e}")
        
        finally:
            if conn:
                conn.close()
if __name__ == "__main__":
    print("Running the auto-mode logic task...")
    auto_mode_logic()
    print("Task finished.")
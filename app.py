from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlite3, random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT id, moisture FROM parameters ORDER BY id DESC LIMIT 10")
    moisture =  [['id', 'moisture']] + list(cur.fetchall())[::-1]
    temp = [['id', 'temp']] + list(cur.execute("SELECT id, temp FROM parameters ORDER BY id DESC LIMIT 10").fetchall())[::-1]
    humidity = [['id', 'humidity']] + list(cur.execute("SELECT id, humidity  FROM parameters ORDER BY id DESC LIMIT 10").fetchall())[::-1]
    water_lvl = [['id', 'water_lvl']] + list(cur.execute("SELECT id, water_lvl FROM parameters ORDER BY id DESC LIMIT 10").fetchall())[::-1]
    current_val = list(cur.execute("SELECT moisture, temp, humidity, water_lvl FROM parameters ORDER BY time DESC LIMIT 1").fetchone())

    con.close()
    
    return render_template('dashboard.html', data=moisture, temp = temp, humidity = humidity, water_lvl = water_lvl ,current_val=current_val)

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
    
@app.route('/fetch_parameters')
def fetch_parameters():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT id , moisture, temp, humidity, water_lvl FROM parameters ORDER BY id DESC LIMIT 10")
    data = cur.fetchall()
    #changeval()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
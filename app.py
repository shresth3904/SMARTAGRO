from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT id, moisture FROM parameters")
    moisture =  [['id', 'moisture']] + list(cur.fetchall())
    temp = [['id', 'temp']] + list(cur.execute("SELECT id, temp FROM parameters").fetchall())
    humidity = [['id', 'humidity']] + list(cur.execute("SELECT id, humidity  FROM parameters").fetchall())
    water_lvl = [['id', 'water_lvl']] + list(cur.execute("SELECT id, water_lvl FROM parameters").fetchall())
    
    con.close()
    
    return render_template('dashboard.html', data=moisture, temp = temp, humidity = humidity, water_lvl = water_lvl)
if __name__ == '__main__':
    app.run(debug=True)
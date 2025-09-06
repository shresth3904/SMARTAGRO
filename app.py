from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>SMART AGRO</h1>"

if __name__ == '__main__':
    app.run(debug=True)
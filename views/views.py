from flask import Flask, request, redirect, flash, send_from_directory, render_template, jsonify, url_for, make_response
from app import *
import flask
import json
import sqlite3

conn = sqlite3.connect('database/database.db', check_same_thread=False)
c = conn.cursor()


@app.route("/", methods=["POST", "GET"])
def index():
    if flask.request.method == 'GET':
        return render_template('dashboard.html')
    else:
        pass
    
@app.route("/service", methods=["GET"])
def service():
    return render_template("service.html")


@app.route("/dashboard", methods=["GET", 'POST'])
def dashboard():
    if flask.request.method == "GET":
        print(request.cookies.get('userID') == 'YT3OYEXU4ANEWU74PUGPTBVHTL3NYXQ7RLPRQADYPNTSSQCMYO4BHMP62Y')
        conn.execute("SELECT * FROM photoColl WHERE owner = ?", (request.cookies.get('userID'), ))
        result = c.fetchall()
        print(result)
        return render_template("dashboard.html")
    return render_template("dashboard.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    if flask.request.method == 'POST':
        data = request.data.decode("utf-8")
        data = json.loads(data)
        
        c.execute("""SELECT * FROM users where userWalletAddr = ?""", (data['addr'], ))
        records = c.fetchall()
        if len(records)==0:
            conn.execute("INSERT INTO users VALUES (?, ?, ?)", (data['type'], data['name'], data['addr']))
            conn.commit()

        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('userID', data['addr'])

        return resp
    


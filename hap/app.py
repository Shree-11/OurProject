from keras.models import model_from_json # Parses a JSON model configuration string and returns a model instance.
from pathlib import Path
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import cv2 # Capturing video using OpenCV
import os
import keras
from glob import glob
import pandas as pd  
import flask
import pickle
from flask import Flask, render_template, request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re
import statistics, requests
from tensorflow.keras.models import load_model
from preprocess import preprocess_image

app=Flask(__name__)

app.secret_key = 'smvitm'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
  
mysql = MySQL(app)

@app.route('/')
def home():

    #pickle.dump(model,open("model1.pkl","wb"))
    
    return flask.render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('main.html', message = message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
        message = ''
        if request.method == 'POST' and 'name' in request.form and 'pwd' in request.form and 'email' in request.form :
             username = request.form['name']
             password = request.form['pwd']
             email = request.form['email']
             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
             account = cursor.fetchone()
             if account:
                  message = 'Account already exists !'
             elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                  message = 'Invalid email address !'
             elif not username or not password or not email:
                  message = 'Please fill out the form !'
             else:
                  cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (username, email, password, ))
                  mysql.connection.commit()
                  message = 'You have successfully registered !'
        elif request.method == 'POST':
             message = 'Please fill out the form !'
        return render_template('signup.html',message = message)

# @app.route('/main', methods=['GET', 'POST'])
# def main():
#     return flask.render_template('main.html')

@app.route('/predict',methods = ['GET','POST'])
def predict():
    class_names = class_names = {
        0:'F',
        1:'M',
        2:'N',
        3:'Q',
        4:'S',
        5:'V'
    }
    if request.method == 'POST':
        # breakpoint()
        file = request.files['file']
    
    # Preprocess the image using your preprocess_image function
        img = preprocess_image(file)
        

    # Load the trained model
        model = load_model('best_model.h5')

        class_prob = model.predict(img)
        class_idx = np.argmax(class_prob)
        class_label = class_names[class_idx]
    
        return render_template('main.html',class_label = class_label)
    
    
if __name__ == "__main__":
    app.run(debug=True)
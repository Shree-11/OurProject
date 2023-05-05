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
from flask import Flask, render_template, request
import statistics, requests
from tensorflow.keras.models import load_model
from preprocess import preprocess_image

app=Flask(__name__)

model = keras.models.load_model('best_model.h5')

@app.route('/')
def home():

    #pickle.dump(model,open("model1.pkl","wb"))
    
    return flask.render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return flask.render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return flask.render_template('signup.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    return flask.render_template('main.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    return flask.render_template('forgotpassword.html')

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
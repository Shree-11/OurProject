from keras.models import model_from_json # Parses a JSON model configuration string and returns a model instance.
from pathlib import Path
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import cv2 # Capturing video using OpenCV
import os
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
    file = request.form['file']
    path = os.path.relpath(file)
    path = os.path.join('u_input',path)
    
    class_names = class_names = {
        0:'F',
        1:'M',
        2:'N',
        3:'Q',
        4:'S',
        5:'V'
    }
    #model = pickle.load(open("model1.pkl","rb"))

    f = Path("models/model_structure.json")
    model_structure = f.read_text()
    model = model_from_json(model_structure) # Parses a JSON model configuration string and returns a model instance.

    
    # loading the trained weights
    model.load_weights("models/model_weights.h5")
    
    #a = os.listdir('u_input')
    
    # removing all other files from the temp folder
    files = glob('temp/*')
    for f in files:
        os.remove(f)
    predict = []
    count = 0
    cap = cv2.VideoCapture(path)   # capturing the video from the given path #not needed
    while(cap.isOpened()):
        # reading from frame 
        ret,frame = cap.read() 
        if ret:
            if count%300 == 0:
                filename = 'temp/'+"_frame%d.jpg" % count;
                # writing the extracted images 
                cv2.imwrite(filename, frame) 
            count+=1
        else: 
                break   
    cap.release() # Closes video file or capturing device.
    cv2.destroyAllWindows() # allows users to destroy all windows at any time.
    # reading all the frames from temp folder
    images = glob("temp/*.jpg")
    prediction_images = []
    for i in range(len(images)):
        img = image.load_img(images[i], target_size=(64,64,3)) #(height,width,rgb) #load image
        img = image.img_to_array(img) #Converts a PIL Image instance to a 3d-array
        img = img/255 #convert rgb(255) to 0-1 value
        prediction_images.append(img)
    # converting all the frames for a test video into numpy array
    prediction_images = np.array(prediction_images)
    y_pred = model.predict(prediction_images, batch_size=1, verbose=0)
    # prediction_images: Number of samples per batch of computation
    # verbose: By setting verbose 0, 1 or 2 you just say how do you want to 'see' the training progress for each epoch.
    # verbose=0 will show you nothing (silent)
    # verbose=1 will show you an animated progress bar.
    # verbose=2 will just mention the number of epoch.
    y_predict = []
    for i in range(0, len(y_pred)):
        y_predict.append(int(np.argmax(y_pred[i])))
    #return jsonify('This video clasify as a ',class_label)
    # The mode of a set of data values is the values that appears most often.
    def most_common(List):
            return statistics.mode(List)
    l = list(y_predict)
    # appending the mode of predictions in predict list to assign the tag to the video
    most_likely_class_index = most_common(l)
    result = class_names[most_likely_class_index]
    return render_template("home.html",result=result)

if __name__ == "__main__":
    app.run(debug=True)
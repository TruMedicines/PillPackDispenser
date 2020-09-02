from flask import Flask, render_template, redirect, url_for, send_file, render_template_string, request, flash
from datetime import datetime, timedelta
from flask import jsonify
from flaskwebgui import FlaskUI
from flask_ask import Ask, statement, question, session
from flask_mail import Message
from flask_mail import Mail
#import CompiledCode as cc
import nextPill 
import time
import csv
import numpy as np
from pyshortcuts import make_shortcut

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
mail = Mail(app)
ask = Ask(app, "/")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
ui = FlaskUI(app, fullscreen=False, maximized=False)


# Set up title, headers, etc for home page
def template(title = "pill web app", text = "Home Page"):
    now = datetime.now()
    timeString = timeStr.strftime("%-I:%M%p")
    today = now.strftime("%A")
    reminderInfo = ["","",""]
    reminderInfo, activateBtn = nextPill.checkNextPillTime(timeString, rmdrFreq)
    dateString = now.strftime("%B %-d, %Y")
    '''
    today8am = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if (activateBtn):
        if (now > today8am):
            activateBtn = True
        else:
            activateBtn = False
    '''

    templateData = {
        'title' : title,
        'time' : reminderInfo[2],
        'day' : reminderInfo[0],
        'text' : text,
        'date' : reminderInfo[1],
        'pillBtn' : activateBtn
        }
    return templateData


# Set home page
@app.route("/")
def home():
    templateData = template()
    return render_template('HomePage.html',**templateData)

@app.route("/takeMeds")
def runDispenser():
    return render_template('loading_page.html')

@app.route("/results")
def results():
    templateData = template()
    nextPill.tookPill()
    return render_template('results.html', **templateData)

@app.route("/contact")
def contact():
    templateData = template()
    return render_template('contact.html', **templateData)

@app.route("/list")
def list():
    templateData = template("Prescription List")
    output = list_csv("medication_list.csv")
    return render_template('medication_list.html', output = output, **templateData)

@app.route("/addMeds")
def addmeds():
    templateData = template("Add Medication")
    output = list_csv("medication_list.csv")
    return render_template('add_meds.html', output=output, **templateData)

#Steve's processing pages
@app.route("/processing")
def processing_home():
    templateData = template()
    return render_template('pillprocessing.html', **templateData)

@app.route("/homebutton")
def home_back():
    templateData = template()
    return render_template('pillprocessing.html', **templateData)

@app.route("/popup")
def popup():
    templateData = template()
    return render_template('popup.html', **templateData)

@app.route("/lit_photo")
def light_photo():
    path = 'lit_photo.jpg'
    return send_file(path)

@app.route("/handle_data", methods=['POST'])
def handle_data():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    print(name)
    print(email)
    print(message)
    msg = Message(message, sender=(name, email),recipients=["charliefisher11@icloud.com"])
    mail.send(msg)
    return render_template('sent_email.html')

def list_csv(csvfile):
    output = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            output.append(row)
        return output

@app.route("/addNewMeds", methods = ['POST'])
def newMeds():
    meds = request.form['meds']
    dose = str(request.form['dose'])
    dose_units = request.form['dose units']
    dose = dose + dose_units
    freq = request.form['freq'] +'\n'
    new_meds = [meds, dose, freq]
    output = list_csv("medication_list.csv")
    duplicate = False 
    for row in output:
        if (np.array_equal(row, new_meds)):
            duplicate = True
            # user typed in same meds return an error
    if not duplicate:
        with open('medication_list.csv','a', newline = '') as f:
            writer=csv.writer(f)
            writer.writerow(new_meds)
    templateData = template("Add Medication")
    new_output = list_csv("medication_list.csv")
    return render_template('add_meds.html', output=new_output, **templateData)

@app.route("/newUser")
def newUser():
    templateData = template("Sign Up")
    return render_template('newUser.html', **templateData)

@app.route("/addNewUser", methods = ['POST'])
def addNewUser():
    templateData = template("Welcome")
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phone = request.form['phone']
    docName = request.form['docName']
    docPhone = request.form['docPhone']
    rmdrHour = request.form['timeHour']
    rmdrMin = request.form['timeMin']
    rmdrDay = request.form['reminderDay']
    rmdrAMPM = request.form['amPm']

    output = list_csv("user_list.csv")
    info = [firstName, lastName, phone, docName, docPhone, rmdrHour, rmdrMin, rmdrAMPM, rmdrDay]
    duplicate = False 
    for row in output:
        if (np.array_equal(row[0:4], info[0:4])):
            duplicate = True
            # user typed in same meds return an error
    if not duplicate:
        with open('user_list.csv','a', newline = '') as f:
            writer=csv.writer(f)
            writer.writerow(info)
    return render_template('confirmSignUp.html', **templateData)

def update_time():
    now = datetime.now()
    time = now.strftime("%-I:%M %p")
    day = now.strftime("%A")
    dateString = now.strftime("%B %-d, %Y")

def get_info():
    csvfile = "user_list.csv"
    output = []
    info = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            output.append(row)
        info = output[-1]
        return info

#Alexa skills portion
@ask.launch
def start_skill():
    welcome_message = 'Hi ' + name + ', what would you like to do?'
    return question(welcome_message)

@ask.intent("DispensePillIntent")
def dispensepills():
    msg = 'Okay, I am dispensing your pills now.'
    return render_template(), iframe = "hello.mp4"
    #return statement(msg)

@ask.intent("ChangePillTimeIntent")
def changepilltime():
    msg = 'Okay, pill time is change to 9:00 am.'
    return statement(msg)
    
@ask.intent("GetPillTimeIntent")
def getpilltime():
    msg = 'Your schedule medication time is at' + Set_Alarm
    return statement(msg)

@ask.intent("AMAZON.CancelIntent")
def cancel():
    msg = 'Okay. Canceling.'
    return statement(msg)

@ask.intent("AMAZON.HelpIntent")
def help():
    msg = 'What do you need help with?'
    return question(msg)

@ask.intent("AMAZON.StopIntent")
def stop_alexa():
    msg = 'Okay. Stopping.'
    return statement(msg)
    
@ask.intent("AMAZON.NavigateHomeIntent")
def go_home():
    msg = 'Okay, navigating you home.'
    return statement(msg), rende

# Gets user info
user = np.empty(8, dtype=object)
user = get_info()
name = user[0]
timeStr = user[5] + user[6] + user[7]
timeStr = datetime.strptime(timeStr,'%I%M%p')
Set_Alarm = timeStr.strftime("%I:%M:%S %p")
rmdrFreq = user[8]



from flask import Flask, render_template, redirect, url_for, send_file, render_template_string, request, flash, jsonify
from datetime import datetime, timedelta
from flask import jsonify
from flaskwebgui import FlaskUI
from flask_ask import Ask, statement, question, session
from flask_mail import Message
from flask_mail import Mail
import time
import csv
import numpy as np
from pyshortcuts import make_shortcut

# ngrok http -hostname=trumedicines.ngrok.io 5000
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
mail = Mail(app)
ask = Ask(app, "/")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
ui = FlaskUI(app, fullscreen=False, maximized=False)

make_shortcut('/Users/Charlie/Desktop/PillPackDispenser/app/app.py', name='Pill Pack Dispenser', icon='/Users/Charlie/Desktop/PillPackDispenser/app/app_icon')

###################################################################################
################################## Webpages #######################################
###################################################################################

# Set up title, headers, etc for home page
def template(title = "pill web app"):
    now = datetime.now()
    timeString = timeStr.strftime("%-I:%M%p")
    today = now.strftime("%A")
    reminderInfo = ["","",""]
    reminderInfo, activateBtn = checkNextPillTime(timeString, rmdrFreq)
    dateString = now.strftime("%B %-d, %Y")

    templateData = {
        'title' : title,
        'time' : reminderInfo[2],
        'day' : reminderInfo[0],
        'date' : reminderInfo[1],
        'pillBtn' : activateBtn
        }
    return templateData

# Set home page
@app.route("/")
def home():
    templateData = template()
    return render_template('HomePage.html',**templateData)

# returns loading page
@app.route("/takeMeds")
def takeMeds():
    return render_template('loading_page.html')

# pill pack results
@app.route("/results")
def results():
    templateData = template()
    tookPill()
    return render_template('results.html', **templateData)

# email contact page
@app.route("/contact")
def contact():
    templateData = template()
    return render_template('contact.html', **templateData)

# for email page
@app.route("/handle_data", methods=['POST'])
def handle_data():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    print(name)
    print(email)
    print(message)
    msg = Message(message, sender=(name, email),recipients=["pillpackdispenser@gmail.com"]) 
    mail.send(msg)
    return render_template('sent_email.html')

# page that lists medication
@app.route("/list")
def list():
    templateData = template("Prescription List")
    output = list_csv("csv_files/medication_list.csv")
    return render_template('medication_list.html', output = output, **templateData)

# page where you can add new medication
@app.route("/addMeds")
def addmeds():
    templateData = template("Add Medication")
    output = list_csv("csv_files/medication_list.csv")
    return render_template('add_meds.html', output=output, **templateData)

#Steve's processing pages
@app.route("/processing")
def processing_home():
    templateData = template()
    return render_template('pill_processing.html', **templateData)

#Steve's processing pages
@app.route("/homebutton")
def home_back():
    templateData = template()
    return render_template('pill_processing.html', **templateData)

#Steve's processing pages
@app.route("/lit_photo")
def light_photo():
    path = 'lit_photo.jpg'
    return send_file(path)
    
# for pill alarm
@app.route("/popup")
def popup():
    templateData = template()
    return render_template('popup.html', **templateData)

# turns csv file into an array to use in other functions
def list_csv(csvfile):
    output = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            output.append(row)
        return output

# adds medications from 'add new medication page' to medication_list.csv
@app.route("/addNewMeds", methods = ['POST'])
def newMeds():
    meds = request.form['meds']
    dose = str(request.form['dose'])
    dose_units = request.form['dose units']
    dose = dose + dose_units
    freq = request.form['freq'] +'\n'
    new_meds = [meds, dose, freq]
    output = list_csv("csv_files/medication_list.csv")
    duplicate = False
    for row in output:
        if (np.array_equal(row, new_meds)):
            duplicate = True
            # user typed in same meds return an error
    if not duplicate:
        with open('csv_files/medication_list.csv','a', newline = '') as f:
            writer=csv.writer(f)
            writer.writerow(new_meds)
    templateData = template("Add Medication")
    new_output = list_csv("csv_files/medication_list.csv")
    return render_template('add_meds.html', output=new_output, **templateData)

# sign up page for new users
@app.route("/newUser")
def newUser():
    templateData = template("Sign Up")
    return render_template('new_user.html', **templateData)

# adds information from /newUser to 'user_list.csv'
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

    output = list_csv("csv_files/user_list.csv")
    info = [firstName, lastName, phone, docName, docPhone, rmdrHour, rmdrMin, rmdrAMPM, rmdrDay]
    duplicate = False
    for row in output:
        if (np.array_equal(row[0:4], info[0:4])):
            duplicate = True
            # user typed in same meds return an error
    if not duplicate:
        with open('csv_files/user_list.csv','a', newline = '') as f:
            writer=csv.writer(f)
            writer.writerow(info)
    return render_template('confirm_sign_up.html', **templateData)

@app.route("/noteTaker")
def addNotes():
    output = list_csv("csv_files/symptom_diary.csv")
    new_symptom = ["date", "symptom"]#add something here
    duplicate = False
    for row in output:
        if (np.array_equal(row, new_symptom)):
            duplicate = True
    if not duplicate:
        with open('csv_files/symptom_diary.csv','a', newline = '') as f:
            writer=csv.writer(f)
            writer.writerow(new_symptom)
    templateData = template("Symptom Note Taker")
    new_output = list_csv("csv_files/symptom_diary.csv")
    return render_template('note_taker.html', output = new_output, **templateData)

###################################################################################
################################## Functions ######################################
###################################################################################

# Gets user info
def get_info():
    csvfile = "csv_files/user_list.csv"
    output = []
    info = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            output.append(row)
        info = output[-1] # gets last entry in csv file
        return info

# return date for next time user should take their pill
def checkNextPillTime(scheduledTime, freq):
    info = []
    pillTimes = []
    lastPill = []
    nextPill = ['', '', '']
    with open("csv_files/pill_timesheet.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            pillTimes.append(row)
    lastPill = pillTimes[-1]

    nowISO = datetime.now()
    #now = now.strftime("%Y%m%d%H%M%S")
    nowDate = nowISO.strftime("%Y%m%d")
                           
    lastISO = datetime(int(lastPill[0]), int(lastPill[1]), int(lastPill[2]), int(lastPill[3]), int(lastPill[4]), int(lastPill[5]))
    lastPill = ''.join([str(elem) for elem in lastPill])
    lastPill = datetime.strptime(lastPill, "%Y%m%d%H%M%S")
    lastDate = lastPill.strftime("%Y%m%d")

    sameDate = (nowDate == lastDate)
    pillBtn = False

    daysLeft = datetime.now() - lastPill
    if (freq == 'daily'):
        if (sameDate):
            nextPill[0] = datetime.now() + timedelta(days = 1)
        else:
            nextPill[0] = datetime.now()
            pillBtn = True
    else: # every other day
        if (sameDate):
            nextPill[0] = datetime.now() + timedelta(days = 2)
        elif (daysLeft == 1):
            nextPill[0] = datetime.now() + timedelta(days = 1)
        else:
            nextPill[0] = datetime.now()
            pillBtn = True
    nextPill[1] = nextPill[0].strftime("%B %-d, %Y")
    nextPill[0] = nextPill[0].strftime("%A")
    nextPill[2] = scheduledTime
    return nextPill, pillBtn
                

def tookPill():
    now = datetime.now()
    timeString = now.strftime("%H%M%S")
    day = now.strftime("%A")
    dateString = now.strftime("%Y%m%d")
    timeAtPill = []
    timeAtPill.append(int(dateString[0:4]))
    timeAtPill.append(int(dateString[4:6]))
    timeAtPill.append(int(dateString[6:8]))
    timeAtPill.append(int(timeString[0:2]))
    timeAtPill.append(int(timeString[2:4]))
    timeAtPill.append(int(timeString[4:6]))
    with open('csv_files/pill_timesheet.csv','a', newline = '') as f:
        writer=csv.writer(f)
        writer.writerow(timeAtPill)

# user information
user = np.empty(8, dtype=object)
user = get_info()
name = user[0]
timeStr = user[5] + user[6] + user[7]
timeStr = datetime.strptime(timeStr,'%I%M%p')
Set_Alarm = timeStr.strftime("%I:%M:%S %p")
rmdrFreq = user[8]

####################################################################
#################### Alexa Skills Portion ##########################
####################################################################
@ask.launch
def start_skill():
    welcome_message = 'Hi ' + name + ', what would you like to do?'
    return question(welcome_message)

@ask.intent("LaunchRequest")
def dispensepills():
    msg = 'Launching'
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
    return statement(msg)

@ask.intent("RecordSymptoms")
def get_symptoms():
    print("here")
    msg = 'Okay, navigating you home.'
    return statement(msg)
   
if __name__ == '__main__':
    ui.run()

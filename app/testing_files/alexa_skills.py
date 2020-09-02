from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode


app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_skill():
    welcome_message = 'Hello there, what would you like to do?'
    return question(welcome_message)

@ask.intent("DispensePillIntent")
def dispensepills():
    msg = 'Okay, I am dispensing your pills now.'
    return statement(msg)

@ask.intent("ChangePillTimeIntent")
def changepilltime():
    msg = 'Okay, pill time is change to 9:00 am.'
    return statement(msg)
    
@ask.intent("GetPillTimeIntent")
def getpilltime():
    msg = 'Your schedule medication time is at 9:00 am.'
    return statement(msg)

@ask.intent("AMAZON.CancelIntent")
def cancel():
    msg = 'Your schedule medication time is at 9:00 am.'
    return statement(msg)

@ask.intent("AMAZON.HelpIntent")
def help():
    msg = 'Your schedule medication time is at 9:00 am.'
    return statement(msg)

@ask.intent("AMAZON.StopIntent")
def stop_alexa():
    msg = 'Your schedule medication time is at 9:00 am.'
    return statement(msg)
    
@ask.intent("AMAZON.NavigateHomeIntent")
def go_home():
    msg = 'Your schedule medication time is at 9:00 am.'
    return statement(msg)

if __name__ == '__main__':
    app.run(debug = True)

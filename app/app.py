from flask import Flask, render_template, redirect, url_for, send_file, render_template_string, request, flash
from datetime import datetime, timedelta
from flask import jsonify
from flaskwebgui import FlaskUI 
from flask_mail import Message
from flask_mail import Mail
from flask_apscheduler import APScheduler
import webbrowser
#import CompiledCode as cc
import time
import csv
import numpy as np
import WebPages as webp
from pyshortcuts import make_shortcut

make_shortcut('/Users/Charlie/Desktop/pill_app/app.py', name='Pill Pack Dispenser',
                        icon='/Users/Charlie/Desktop/pill_app/app_icon')

if __name__ == '__main__':
    webp.app.run(debug = True)

 

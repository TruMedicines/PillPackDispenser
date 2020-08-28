from flask import Flask, render_template, redirect, url_for, send_file, render_template_string, request, flash
from datetime import datetime, timedelta
from flask_lambda import FlaskLambda
from flask import jsonify
from flaskwebgui import FlaskUI 
#from flask_mail import Message
#from flask_mail import Mail
from flask_apscheduler import APScheduler
import webbrowser
#import CompiledCode as cc
import time
import csv
import numpy as np
import WebPages as webp
from pyshortcuts import make_shortcut
import boto3
from botocore.config import Config
from pydub import AudioSegment

make_shortcut('/Users/Charlie/Desktop/PillPackDispenser/app/app.py', name='Pill Pack Dispenser',
                        icon='/Users/Charlie/Desktop/PillPackDispenser/app/app_icon')

my_config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

client = boto3.client('polly', config=my_config)
text = "hello there"
response = client(Text=text, VoiceId='Salli', OutputFormat='mp3')


if __name__ == '__main__':
    webp.app.run()

 

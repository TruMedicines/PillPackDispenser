from flask import Flask, render_template, redirect, url_for, send_file, render_template_string, request, flash, g
from datetime import datetime, timedelta
from flask import jsonify
from functools import wraps
from urllib import request as web_request
from jose import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Set home page
@app.route("/")
@aws_amplify_login_required
def home():
    user = request.user
    return f'Hello, {user}'

import os
from twilio.rest import Client
from datetime import datetime, timedelta

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

now = datetime.now()
takenPill = False # get this info from app.py
scheduled_time = now.replace(hour=8, minute=0, second=0, microsecond=0) #change this to scheduled time
if (now > scheduled_time and takenPill): # time is past scheduled time
    message = client.messages \
    .create(
         body="Hello. This is your pill pack dispenser, reminding you to take you pill.",
         messaging_service_sid='MG027cd6ecec3d65482635b712b31e65db',
         to='+17026240639'
     )

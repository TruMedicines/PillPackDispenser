from flask import Flask
from flask_apscheduler import APScheduler
import webbrowser
import time

app = Flask(__name__)
scheduler = APScheduler()
Set_Alarm = str('02:24:00PM')

def alarm():
    
    url = str('https://stackoverflow.com/questions/35168508/raw-input-is-not-defined')

    # This is the actual time that we will use to print.
    Actual_Time = time.strftime("%I:%M:%S%p")
     
    # This is the while loop that'll print the time
    # until it's value will be equal to the alarm time
    if (Actual_Time != Set_Alarm):
        print("The time is " + Actual_Time)
        Actual_Time = time.strftime("%I:%M:%S%p")
        time.sleep(1)
     
    # This if statement plays the role when its the
    # alarm time and executes the code within it.
    if (Actual_Time == Set_Alarm):
        print("You should see your webpage now :-)")
     
        # We are calling the open()
        # function from the webrowser module.
        webbrowser.open(url)
    
if __name__ == '__main__':
    scheduler.add_job(id = 'scheduled task', func = alarm, trigger = 'cron', minute = '0-59', second = '0')
    scheduler.start()
    webbrowser.open_new("http://127.0.0.1:5000/")
    app.run(debug=True, host = '0.0.0.0')

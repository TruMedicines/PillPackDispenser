import time
from datetime import datetime, timedelta
import csv

def checkNextPillTime(scheduledTime, freq):
    info = []
    pillTimes = []
    lastPill = []
    nextPill = ['', '', '']
    with open("pill_timesheet.csv", 'r') as f:
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
    '''
    with open("medication_list.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            info.append(row)
        for i in info:
            string = i[2]
            string = string[:-1]
            freq.append(string)
    '''
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
    with open('pill_timesheet.csv','a', newline = '') as f:
        writer=csv.writer(f)
        writer.writerow(timeAtPill)

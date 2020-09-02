from datetime import datetime
import time
import serial
from time import sleep
#import pill_analyzer as pa
#import pill_segmenter as ps
from picamera import PiCamera
#import cv2


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
# SETUP
print("Setting up system")
#seg = ps.PillSegmenter()
#an = pa.PillAnalyzer()
#seg.thresh_thresh = 100 #100-170
#seg.circle_thresh = 8 #11 is default
print("Finished Setup")

def sendByte(sentence, ser):
        sentence = sentence + "\n"
        ser.write(sentence.encode('ascii'))

def readByte(sentence, ser):
        line = ""
        while line != sentence:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()


def takePhotos(ser): # takes photos of next day's pills
        # backlight photo
        readByte("backlight on", ser)

        with PiCamera() as camera:
                camera.resolution=(3280,2464)
                print("Taking contour photo")
                time.sleep(2)
                camera.capture('rpi_photo.jpg')
                print("took contour photo")
                # front light photo
                sendByte("took contour", ser)
                readByte("front light on", ser)
                print("Taking bright photo")
                time.sleep(2)
                camera.capture('lit_photo.jpg')
                print("took front photo")
                # send confirmation
                sendByte("took front photo", ser)

'''
def segmentation():
        seg.original_image = cv2.imread('rpi_photo.jpg')
        seg.bright_image = cv2.imread('lit_photo.jpg')
        num_pills = seg.segment_pills(debug_mode=True)
        return num_pills

def analysis(num_pills):
        print("Analyzing pill(s)")
        an.qr_image = cv2.imread('images/qr_code.jpg')
        print("QR code: %s" %an.decode_qr())
        for i in range(num_pills):
                enc = an.encode_pill('images/lit_pill' + str(i) + '.jpg')
                print("Encoding:", enc)
'''      
def scan_pill():
        time.sleep(3) # need a delay to send first byte
        sendByte("on", ser)
        print("starting test")
        takePhotos(ser)
        # add Steve's imaging processing stuff here
        #num_pills = segmentation()
        # analysis(num_pills)
        print("done")
        time.sleep(5)
        #return num_pills

if __name__ == '__main__':
        
        while True:
                time.sleep(3) # need a delay to send first byte
                sendByte("on", ser)
                print("starting test")
                takePhotos(ser)
                # add Steve's imaging processing stuff here
               # num_pills = segmentation()
#                analysis(num_pills)
                print("done")
                time.sleep(5)

            
"""
Some of this code will be added once the webapp stuff is completed

bool sentConfirmation = False 

def sendReminder(): # add from Zhongyi's code

def confirmTakePills(): # receive notice from web app that the user agrees to take pills.
        return takePills # bool
while 1 :
        now = datetime.now()
        currTime = int(now.strftime("%H%M%S")) # 24 hr clock
        schedTime = currTime # filler for now. Will be an input time from user.
        if (schedTime == currTime): # can also add an OR statement that adds receivedReminder
                
                sendReminder() 
                while not sentConfirmation:
                        sentConfirmation = confirmTakePills

                sentConfirmation = False # reset boolean for tomorrow's meds
                
                # send code to Arduino to send pills
                # while loop reading from Arduino
                        # Arduino sends signals that says pill is dipense and backlight is lit
                
                # at this point, the packet should have dispensed to the user right now
                takePhotos()
                
                # do other imaging stuff here. Add steve's code.
                time.sleep(1000)
"""

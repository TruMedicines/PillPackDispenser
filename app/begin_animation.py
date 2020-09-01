import subprocess
import os
import WebPages as webp

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def check_current_audio():
    dir_path = os. getcwd()
    print(dir_path)
    hello = find_all("hello.mp3", "animation_audio")
    getpilltime = find_all("getpilltime.mp3", "animation_audio")
    dispense = find_all("dispense.mp3", "animation_audio")
    
    if not hello:
        #creates speech with Amazon Polly
        text = '"Hi "' + webp.name + '". How can I help you?"'
        command = 'aws polly synthesize-speech --output-format "mp3" --engine neural --voice-id "Salli" --text '
        filename = ' audio_files/hello.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)
        
        #creates talking avatar from speech
        

    if not dispense:
        text = '"Okay, I am dispensing your pills now."'
        command = 'aws polly synthesize-speech --output-format "mp3" --engine neural --voice-id "Salli" --text '
        filename = ' audio_files/dispense.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)

    if not getpilltime:
        text = '"Your scheduled medication time is at {}"'.format(webp.Set_Alarm)
        command = 'aws polly synthesize-speech --output-format "mp3" --engine neural --voice-id "Salli" --text '
        filename = ' audio_files/getpilltime.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)

check_current_audio()


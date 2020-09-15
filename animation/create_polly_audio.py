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
    # finds all audio files in 'animaiton_audio' folder
    hello = find_all("hello.mp3", "animation_audio")
    confirm = find_all("confirm.mp3", "animation_audio")
    dispense = find_all("dispense.mp3", "animation_audio")
    thankyou = find_all("thankyou.mp3", "animation_audio")
    
    if not hello: # if there is no file in the folder, create the animation
        #creates speech with Amazon Polly
        text = '"<speak> Good morning Bruce Johnson. I am Traci, your medication assistant. It is 8am and time to take your pill packet. <break time = \'300ms\'/>  </speak>"'
        command = 'aws polly synthesize-speech --text-type "ssml" --output-format "mp3" --engine neural --voice-id "Emma" --text '
        filename = ' animation_audio/hello.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)
        
    if not dispense:
        text = '"<speak> Your pill packet has been dispensed. Please confirm by pressing the OK button. I will make a note of the time and date for you. <break time = \'300ms\'/>. </speak>"'
        command = 'aws polly synthesize-speech --text-type "ssml" --output-format "mp3" --engine neural --voice-id "Emma" --text '
        filename = ' animation_audio/dispense.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)

    if not confirm:
        text = '"<speak>Please confirm Pill Packet, with big green OK button <break time = \'300ms\'/> </speak>"'
        command = 'aws polly synthesize-speech --text-type "ssml" --output-format "mp3" --engine neural --voice-id "Emma" --text '
        filename = ' animation_audio/confirm.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)
        
    if not thankyou:
        text = '"<speak>Thank you Bruce. I will see you again tomorrow. Stay healthy. Bye for now. <break time = \'300ms\'/> </speak>"'
        command = 'aws polly synthesize-speech --text-type "ssml" --output-format "mp3" --engine neural --voice-id "Emma" --text '
        filename = ' animation_audio/thankyou.mp3'
        command = command + text + filename
        subprocess.call(command, shell=True)

check_current_audio()


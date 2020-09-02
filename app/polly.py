import subprocess

command = 'aws polly synthesize-speech --output-format "mp3" --voice-id "Salli" --text "hello, my name is Joe. Nice to meet you" hello.mp3'

subprocess.call(command, shell=True)



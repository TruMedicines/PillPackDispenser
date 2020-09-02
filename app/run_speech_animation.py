import sda
import scipy.io.wavfile as wav
import os, sys
from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--input", required=True, help="audio to render")
parser.set_defaults(verbose=False)
opt = parser.parse_args()
audio_file = opt.input
dir_audio = "animation_audio/" + audio_file + ".mp3"

va = sda.VideoAnimator(gpu=-1, model_path="grid")# Instantiate the animator

vid, aud = va("animation_images/image.bmp", dir_audio)

output_file = "first-order-model-master/driver_videos/" + audio_file + ".mp4"
va.save_video(vid, aud, output_file)

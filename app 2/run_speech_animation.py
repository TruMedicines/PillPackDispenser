import sda
import scipy.io.wavfile as wav
import os, sys
from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--input", required=True, help="audio to render")
parser.set_defaults(verbose=False)
opt = parser.parse_args()
print(opt)

va = sda.VideoAnimator(gpu=-1, model_path="grid")# Instantiate the animator

vid, aud = va("example/image.bmp", "example/audio/speech1.mp3")

va.save_video(vid, aud, "../first-order-model-master/images/driver.mp4")

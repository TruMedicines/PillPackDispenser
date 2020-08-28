import sda
import scipy.io.wavfile as wav
import os, sys
from PIL import Image
from argparse import ArgumentParser

va = sda.VideoAnimator(gpu=-1, model_path="timit")# Instantiate the animator

vid, aud = va("example/image.bmp", "example/audio/speech1.mp3")

va.save_video(vid, aud, "../first-order-model-master/images/driver.mp4")

#!/usr/bin/env python
import cv2
import numpy as np
from time import sleep
from pylibdmtx import pylibdmtx
import keras
from keras.models import Model, load_model
from keras.layers import GlobalAveragePooling2D
import time
import Cartesian2Polar
from PIL import Image


class PillAnalyzer:
    def __init__(self):
	    self.qr_image = None
	    self.encoder = self.load_model()
		
    def decode_qr(self):
	    dec = pylibdmtx.decode(self.qr_image)
	    return dec
	    
    def load_model(self, model_name='models/borg_keras.h5'):
	    print("Loading model")
	    t0 = time.time()
	    autoencoder = load_model(model_name)
	    encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoder').output)
	    t1 = time.time()
	    print("Model loaded in: ", t1-t0)
	    enc_model = Model(autoencoder.input, autoencoder.get_layer('encoder').output)
	    x1 = enc_model.get_layer('encoder').output
	    x1 = GlobalAveragePooling2D(name='flat')(x1)
	    encoder = Model(enc_model.input, x1)
	    return encoder
	
    def expand_for_encoding(self, img):
	    single = cv2.resize(img, (128,64))
	    single = np.expand_dims(single, axis=2)
	    single_scaled = single * 1. / 255
	    single_scaled = np.expand_dims(single_scaled, axis=0)
	    return single_scaled
	
    def encode_pill(self, src):
	    im = Image.open(src)
	    pim = Cartesian2Polar.project_cartesian_image_into_polar_image(im, origin=None)

	    crop_height = min(150, pim.height)
	    crop_width = min(10000, pim.width)
	    cropped_polar_im = pim.crop(box=(0,0,crop_width,crop_height))

	    open_cv_image = np.array(cropped_polar_im)
	    open_cv_image = open_cv_image[:,:,::-1].copy()
	    img = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

	    img = self.expand_for_encoding(img)
	    encoding = self.encoder.predict(img, batch_size=1)
	    return encoding

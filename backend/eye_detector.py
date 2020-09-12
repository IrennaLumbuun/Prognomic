import sys
import json
from keras.models import load_model
from PIL import Image
import cv2
import numpy as np

# Imports the Google Cloud client library
from google.cloud import vision
from google.protobuf.json_format import MessageToDict

client = vision.ImageAnnotatorClient()
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml')


def detect_eyes(image):
    img = Image.open(image)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(img)
    crop_boundary = list()
    for (ex, ey, ew, eh) in eyes:
        bound = [ex, ey, ex + ew, ey + eh]
        crop_boundary.append(bound)
    print(crop_boundary)
    return crop_boundary


def handle_image(image):
    img_copy = image  # safe a copy of the image for future use (e.g cropping)
    crop_boundary = detect_eyes(img_copy)
    images = list()  # replace with a list of cropped & resized image

    # crop image and reshape images
    im = Image.open(img_copy)
    for bounds in crop_boundary:
        eye = im.crop((bounds[0], bounds[1], bounds[2], bounds[3]))
        # resize & convert to grayscale
        eye = np.array(eye)
        eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
        eye = cv2.resize(eye, (151, 332))

        images.append(eye)

    # pass to model
    model = load_model('backend/trained_dataset.h5')
    interpret = ["cat", "bulk", "crossed"]
    result = dict()
    for img in images:
        img = img.reshape((1, 50132)).tolist()
        output = model.predict(img)
        output = output.flatten().tolist()
        for i in range(len(interpret)):
            result[interpret[i]] = output[i]
        print(result)
    return result

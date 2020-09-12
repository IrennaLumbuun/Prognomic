import sys
import json
#import cv2
#import numpy as np
#from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision
from google.protobuf.json_format import MessageToDict

client = vision.ImageAnnotatorClient()


def handle_image(image):
    # save nd array
    # convert to b64

    # get_eyes position
    eyes_pos = get_eyes()
    crop_boundary = get_crop_boundary(eyes_pos)

    # crop image

    # pass to model


def get_crop_boundary(eyes_pos):
    crop_boundary = list()
    for pos in eyes_pos:
        bound = list()
        # left eye
        if pos.get('left_eye', None) != None:
            # left eye exists
            upper_left_left_eye = [pos.get('left_eye_left_corner')[
                'x'], pos.get('left_eye_top_boundary', 0)['y']]
            bottom_right_left_eye = [pos.get('left_eye_right_corner')[
                'x'], pos.get('left_eye_bottom_boundary', 0)['y']]
        # right eye
        if pos.get('right_eye', None) != None:
            # right eye exists
            upper_left_right_eye = [pos.get('right_eye_left_corner')[
                'x'], pos.get('right_eye_top_boundary', 0)['y']]
            bottom_right_right_eye = [pos.get('right_eye_right_corner')[
                'x'], pos.get('right_eye_bottom_boundary', 0)['y']]

            bound.append(upper_left_left_eye)
            bound.append(bottom_right_left_eye)
            bound.append(upper_left_right_eye)
            bound.append(bottom_right_right_eye)
            if len(bound != [] and len(bound) % 2 == 0):
                crop_boundary.append(bound)
    return crop_boundary


def get_eyes():
    # request placeholder
    request = {
        'image': {
            'source': {
                'image_uri': 'https://preview.redd.it/4t5n1ynrhjm51.jpg?width=720&format=pjpg&auto=webp&s=a7f4c3d0af3b405126ed11c5c5dee0bb8f84ec25'
            },
        },
    }
    # parse response
    response = client.annotate_image(request)
    response = MessageToDict(response)

    faces = response['faceAnnotations']
    eyes_pos = list()  # save coordinate of left eye and right eye

    info_needed = ['LEFT_EYE', 'RIGHT_EYE', 'RIGHT_EYE_LEFT_CORNER', 'RIGHT_EYE_BOTTOM_BOUNDARY',
                   'RIGHT_EYE_RIGHT_CORNER', 'RIGHT_EYE_TOP_BOUNDARY', 'LEFT_EYE_LEFT_CORNER', 'LEFT_EYE_BOTTOM_BOUNDARY',
                   'LEFT_EYE_RIGHT_CORNER', 'LEFT_EYE_TOP_BOUNDARY']

    for face in faces:
        landmark_pos = dict()
        try:
            landmarks = face['landmarks']
            for landmark in landmarks:
                landmark_type = landmark.get('type', '')
                if landmark_type in info_needed:
                    landmark_pos[landmark_type.lower()] = landmark['position']
            eyes_pos.append(landmark_pos)
        except Exception as e:
            print('--------errror---------')
            print(response)
            print(e)
            return eyes_pos

    return eyes_pos


print("----------------------")
handle_image(None)

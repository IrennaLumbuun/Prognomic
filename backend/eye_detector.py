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


def handle_image(image):
    img_copy = image  # safe a copy of the image for future use (e.g cropping)
    b64_image = image.read()  # decoded image

    # get_eyes position
    eyes_pos = get_eyes(b64_image)

    if eyes_pos == []:
        return "Can't find face"

    # crop boundary consits of [(upper left left eye), (bottom right right eye), (upper left right eye), {bottom right tight eye}]
    crop_boundary = get_crop_boundary(eyes_pos)

    images = list()  # replace with a list of cropped & resized image

    # crop image and reshape images
    im = Image.open(img_copy)
    for bounds in crop_boundary:
        # crop
        left_eye = im.crop((bounds[0][0], bounds[0][1],
                            bounds[1][0], bounds[1][1]))
        # resize & convert to grayscale
        left_eye = np.array(left_eye)
        left_eye = cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)
        left_eye = cv2.resize(left_eye, (151, 332))

        images.append(left_eye)
        if len(bounds) == 4:
            right_eye = im.crop((
                bounds[2][0], bounds[2][1], bounds[3][0], bounds[3][1]))
            # resize & convert to grayscale
            right_eye = np.array(right_eye)
            right_eye = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
            right_eye = cv2.resize(right_eye, (151, 332))

    # pass to model
    model = load_model('backend/trained_dataset.h5')
    result = {
        "crossed eye or cataract": ""
    }
    for img in images:
        img = img.reshape((1, 50132)).tolist()
        output = model.predict(img)
        output = output.flatten().tolist()
        if output[0] > 0.9 or output[1] > 0.9 or output[2] > 0.9:
            result['crossed eye or cataract'] = 'Very Likely'
        elif output[0] > 0.8 or output[1] > 0.8 or output[2] > 0.8:
            result['crossed eye or cataract'] = 'Likely'
        else:
            result['crossed eye or cataract'] = 'Unlikely'

    return result


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
            if bound != [] and len(bound) % 2 == 0:
                crop_boundary.append(bound)
    return crop_boundary


def get_eyes(b64_image):
    request = {
        'image': {
            'content': b64_image
        },
        'features': [{
            'type': vision.enums.Feature.Type.FACE_DETECTION
        }]
    }
    # parse response
    response = client.annotate_image(request)
    response = MessageToDict(response)

    try:
        faces = response['faceAnnotations']
    except:
        print("No face")
        return list()
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

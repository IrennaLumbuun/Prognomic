import pyrebase
import requests
import uuid
from flask import *
from backend.eye_detector import handle_image
import base64

# twilio
from backend.twilio_credentials import account_sid, auth_token, twilio_cell
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Authentication data for Firebase
config = {
    "apiKey": "AIzaSyChXIzSdDfONoykC2TnHYAlirUiWZ5cN10",
    "authDomain": "docassist-b11a1.firebaseapp.com",
    "databaseURL": "https://docassist-b11a1.firebaseio.com",
    "projectId": "docassist-b11a1",
    "storageBucket": "docassist-b11a1.appspot.com",
    "messagingSenderId": "745447706751",
    "appId": "1:745447706751:web:9d3a3fd9d36f3fe6b9af4a",
    "measurementId": "G-K7KNNBZF3S"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# twilio config
twilio_client = Client(account_sid, auth_token)

# Start Flask app
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def welcome():
    return 'Hello, user!'

# Add a new user


@app.route("/register", methods=['POST', 'GET'])
def register():
    idx = str(uuid.uuid1())
    username = request.args.get('username')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    password = request.args.get('password')
    age = request.args.get('age')
    db.child("users").push({
        "id": idx,
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "password": password,
        "age": age,
    })
    return "Post succeded"

# Return data about user at login


@app.route("/login", methods=['GET'])
def login():

    users = db.child("users").get()
    username = request.args.get('username')
    password = request.args.get('password')
    users = db.child("users").get()
    result = users.val()

    for k, v in result.items():
        if str(v["username"]) == username and str(v["password"]) == password:
            return v

    return "Login Failed"

# helper method


def get_user_from_username(username):
    users = db.child("users").get()
    for k, v in users.val().items():
        if str(v.get("username", "")) == username:
            return k, v
    return None, dict()


# Retrieve information to show on health report
@app.route("/report", methods=["GET"])
def get_report():
    body = request.json
    username = body.get('username', '')

    # get users info
    _, user = get_user_from_username(username)
    if user == {}:
        return "User not found"
    else:
        return {
            "age": user.get("age", None),
            "gender": user.get("gender", None),
            "email": user.get("email", None),
            "firstname": user.get("firstname", None),
            "lastname": user.get("lastname", None),
            "picture": user.get("picture", None),
            "analysis": user.get("analysis", None),
        }

# send notification to the doctor when users upload picture


def send_notification(phone_number, first_name, last_name):
    patient_name = f'{first_name} {last_name}'

    if phone_number != None:
        twilio_client.messages.create(
            body=f"Hi, {patient_name} just uploaded a picture. A report has been generated.",
            from_=twilio_cell,
            to=phone_number,
        )
    return 200

# Apply model for cataract, crossed eye, bulk eye


@ app.route("/upload", methods=['POST'])
def post_eye_abnormality():
    body = request.form.to_dict(flat=False)
    username = body.get("username", [""])[0]

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No files selected"

        user_photo = request.files['file']
        if user_photo.filename == '':
            return "No photo selected"

        valid_extension = allowed_file(user_photo.filename)
        if not valid_extension:
            return 'Extension is not valid. Only allow .png, .jpg, and .jpeg'

        if user_photo and valid_extension:
            b64_image, output = handle_image(user_photo)
            # output is a list consisting of probability that the person has abnormal eye congition
            if len(output) > 0:
                # save output
                key, user = get_user_from_username(username)
                user['analysis'] = output
                user['picture'] = base64.b64encode(b64_image).decode('utf-8')
                db.child("users").child(key).set(user)

                # notify doctor
                send_notification("+18059007177", user.get('firstname',
                                                           'no-first-name'), user.get('lastname', 'no-last-name'))
                return output
            else:
                return "Can't find an eye in the picture."
    return 404  # error


def allowed_file(filename) -> bool:
    _allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in _allowed_extensions


@app.route("/send_report", methods=['POST'])
def send_report():
    # do something
    return


if __name__ == '__main__':
    app.run(debug=True)

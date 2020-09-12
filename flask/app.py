import pyrebase
import uuid
from flask import *

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

#Start Flask app
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

#Return data about user at login
@app.route("/login", methods=['GET'])
def login():
	
	users = db.child("users").get()
	username = request.args.get('username')
	password = request.args.get('password')
	users = db.child("users").get()
	result = users.val()

	for k,v in result.items():
		if str(v["username"]) == username and str(v["password"]) == password:
			return v

	return "Login Failed"

if __name__ == '__main__':
	app.run(debug=True)

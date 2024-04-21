'''
app.py contains all of the server application
this is where you'll find all of the get/post request handlers
the socket event handlers are inside of socket_routes.py
''' 


import bcrypt
from flask import Flask, render_template, request, abort, url_for
from flask_socketio import SocketIO
import db
import secrets
import encyrption

# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
socketio = SocketIO(app)

# don't remove this!!
import socket_routes

# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")

    user = db.get_user(username)
    if user is None:
        return "Error: User does not exist!"
    
    if not bcrypt.checkpw(request.json.get("password").encode('utf-8'), user.password):
        return "Error: Password does not match!"        

    return url_for('home', username=request.json.get("username"))

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    bits = 10,
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = bcrypt.hashpw(request.json.get("password").encode('utf-8'), bcrypt.gensalt())
    privateKey = encyrption.privateKey(bits[0])
    print(privateKey)

    if db.get_user(username) is None:
        db.insert_user(username, password, privateKey)
        return url_for('home', username=username)
    return "Error: User already exists!"

# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/home")
def home():
    if request.args.get("username") is None:
        abort(404)
<<<<<<< HEAD
    activ_user = db.get_conn_user()
    return render_template("home.jinja", username=request.args.get("username"),connected_users=activ_user)
=======

    username = request.args.get("username")

    matches = db.friends_received(username)
    requests = db.show_friends_sent(username)
    friends_list = db.show_friends_list(username)

    return render_template("home.jinja", username=username, 
                           matches=matches, requests=requests, friendsList=friends_list)


# all functions for friends and requests:

#function to send friends reqursts
@app.route('/friend_request', methods=['POST'])
def add_friend():
    friend = request.form.get('friend')
    sender = request.form.get('username')
    db.friend_request(sender, friend) 
    return ('Friend request sent successfully!')    

#cancel a friends request
@app.route('/delete_request', methods=['POST'])
def delete_user():
    friend = request.form.get('friend')
    username = request.form.get('username')
    db.cancel_request(username, friend)
    return ('Request deleted successfully')  

#show friends
@app.route('/friends_list', methods=['POST'])
def friends():
    friend1 = request.form.get('friend1')
    friend2 = request.form.get('friend2')
    db.friends(friend1, friend2) 
    return ('Friend added!')    

#remove friends 
@app.route('/remove_friends', methods=['POST'])
def remove_friends():
    user = request.form.get('user')
    friend = request.form.get('friend')
    print(user, friend)
    result = db.remove_friends(user, friend) 
    return result   
>>>>>>> friend_requests


if __name__ == '__main__':
    ssl_cert = 'certs/info2222.crt'  # SSL certificate file
    ssl_key = 'certs/info2222.key'   # SSL private key file
    socketio.run(app, host='127.0.0.1', port=5000, ssl_context=(ssl_cert, ssl_key))

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
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = bcrypt.hashpw(request.json.get("password").encode('utf-8'), bcrypt.gensalt())

    if db.get_user(username) is None:
        db.insert_user(username, password)
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
    return render_template("home.jinja", username=request.args.get("username"))


@app.route('/friend_request', methods=['POST'])
def add_friend():
    friend = request.form.get('friend')
    sender = request.form.get('username')
    db.friend_request(sender, friend) 
    return ('Friend request sent successfully!')    

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(sender, friend)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    ssl_cert = 'certs/info2222.crt'  # SSL certificate file
    ssl_key = 'certs/info2222.key'   # SSL private key file
    socketio.run(app, host='127.0.0.1', port=5000, ssl_context=(ssl_cert, ssl_key))

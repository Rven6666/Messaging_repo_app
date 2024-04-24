'''
socket_routes
file containing all the routes related to socket.io
'''


from flask_socketio import join_room, emit, leave_room
from flask_login import current_user, logout_user
from flask import request, session

try:
    from __main__ import socketio
except ImportError:
    from app import socketio

from models import Room

import db

room = Room()

# when the client connects to a socket
# this event is emitted when the io() function is called in JS

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@socketio.on('connect')
def connect(auth=None):
    username = request.cookies.get("username")
    room_id = request.cookies.get("room_id")
    logger.debug(f"socket: User {username} is attempting to connect.")
    if not current_user.is_authenticated:
        logger.debug(f"User {username} is identified as unauthorized.")
        disconnect()
        return 'Unauthorized!'
    db.update_conn(username,True)
    update_conn_stats()# call update in frontend userLs
    
    if room_id is None or username is None:
        logger.debug("Missing room_id or username. room_id: %s, username: %s", room_id, username)
        return
    # socket automatically leaves a room on client disconnect
    # so on client connect, the room needs to be rejoined
    logger.debug(f"{username} has re-connected to {room_id}")
    join_room(int(room_id))
    emit("incoming", (f"{username} has connected", "green"), to=int(room_id))


# event when client disconnects
# quite unreliable use sparingly


@socketio.on('disconnect')
def disconnect():
    username = request.cookies.get("username")
    room_id = request.cookies.get("room_id")
    db.update_conn(username,False)
    logger.debug(f"Socket: User {username} is disconnected.")
    update_conn_stats() # call update in frontend userLs
    logout_user()
    session.pop(room_id, None)
    if room_id is None or username is None:
        return
    emit("incoming", (f"{username} has disconnected", "red"), to=int(room_id))
    

# send message event handler


@socketio.on("send")
def send(username, message, room_id):
    emit("incoming", (f"{username}: {message}"), to=room_id)

# join room event handler
# sent when the user joins a room


@socketio.on("join")
def join(sender_name, receiver_name):

    receiver = db.get_user(receiver_name)
    if receiver is None:
        return "Unknown receiver!"

    sender = db.get_user(sender_name)
    if sender is None:
        return "Unknown sender!"

    room_id = room.get_room_id(receiver_name)

    # if the user is already inside of a room
    if room_id is not None:

        room.join_room(sender_name, room_id)
        join_room(room_id)
        # emit to everyone in the room except the sender
        emit("incoming", (f"{sender_name} has joined the room.",
             "green"), to=room_id, include_self=False)
        # emit only to the sender
        emit(
            "incoming", (f"{sender_name} has joined the room. Now talking to {receiver_name}.", "green"))
        return room_id

    # if the user isn't inside of any room,
    # perhaps this user has recently left a room
    # or is simply a new user looking to chat with someone
    room_id = room.create_room(sender_name, receiver_name)
    join_room(room_id)
    emit("incoming",
         (f"{sender_name} has joined the room. Now talking to {receiver_name}.", "green"), to=room_id)
    return room_id

# leave room event handler


@socketio.on("leave")
def leave(username, room_id):
    emit("incoming", (f"{username} has left the room.", "red"), to=room_id)
    leave_room(room_id)
    room.leave_room(username)

def update_conn_stats():# call update in frontend userLs
    logger.debug(f"\nsocket: called update in frontend.\n")
    db_received_activ_users = [{"username": user.username} for user in db.get_conn_user()]
    socketio.emit('update_user_stats', {'connected_users': db_received_activ_users}, namespace='/')
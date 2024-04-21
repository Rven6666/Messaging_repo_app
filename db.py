'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from models import * 
# from models import FriendRequest
from pathlib import Path
import random
import sympy
import bcrypt

# creates the database directory
Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
Base.metadata.create_all(engine)

# inserts a user to the database
def insert_user(username: str, password: str, privateKey: int):
    with Session(engine) as session:
        user = User(username=username, password=password, privateKey=privateKey)
        session.add(user)
        session.commit()

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)

<<<<<<< HEAD
def get_conn_user():
    """
    Retrieve a list of connected users from the database.

    This function establishes a session with the provided SQLAlchemy engine,
    queries the 'User' table for users who are currently connected,
    and prints their usernames and connection status. It then returns
    a list of User objects representing the connected users.

    Returns:
        list: A list of User objects representing connected users.
    """
    with Session(engine) as session:
        connected_users = session.query(User).filter(User.is_conn == True).all()
        for user in connected_users:
            print(f"Username: {user.username}, Connected: {user.is_conn}")
        return connected_users

def update_conn(username, is_connected):
    """
    Update the user's connection status in the database.

    Parameters:
    username (str): The username of the user.
    is_connected (bool): True if the user is connected, False otherwise.
    """
    with Session(engine) as session:
        stmt = (
        update(User).
        where(User.username == username).
        values(is_conn=is_connected)
        )
    session.execute(stmt)
    session.commit()
    print(f"conn_status updated for {username} to {is_connected}")

def friendRequest(username: str, friend: str):
=======
def friend_request(sender: str, receiver: str):
>>>>>>> friend_requests
    with Session(engine) as session:
        request = FriendRequest(sender=sender, receiver=receiver)
        session.add(request)
        session.commit()

def cancel_request(sender: str, receiver: str):
    print('cancel request function db')
    with Session(engine) as session:
        request_to_delete = session.query(FriendRequest).filter_by(sender=sender, receiver=receiver).first()
        if request_to_delete:
            session.delete(request_to_delete)
            session.commit()
            return 'Request deleted'
        else:
            return 'No matching friend request found'

def friends_received(username: str):
    with Session(engine) as session:
        results = session.query(FriendRequest.sender).filter_by(receiver=username).all()
        return [row[0] for row in results]
      
def show_friends_sent(username: str):
    with Session(engine) as session:
        # Query to retrieve all rows where column_two matches column_one
        requests = session.query(FriendRequest.receiver).filter(FriendRequest.sender == username).all()
        # Extracting just the values from the tuples
        return [row[0] for row in requests]

def friends(friend1: str, friend2: str):
    with Session(engine) as session:
        request = FriendList(friend1=friend1, friend2=friend2)
        session.add(request)
        session.commit()

def remove_friends(user: str, friend: str):
    print('remove friends fucntion db')
    with Session(engine) as session:
        relationship_delete = session.query(FriendList).filter_by(friend1=user, friend2=friend).first()
        if relationship_delete:
            session.delete(relationship_delete)
            session.commit()
            return 'Friend deleted'
        else:
            return 'No relationship found.'
        
def show_friends_list(username: str):
    with Session(engine) as session:
        # friendships column 1
        column1 = session.query(FriendList.friend2).filter(FriendList.friend1 == username).all()

        # friendships column 2
        column2 = session.query(FriendList.friend1).filter(FriendList.friend2 == username).all()

        # compare and match for each column
        friendships_column1 = [row[0] for row in column1]
        friendships_column2 = [row[0] for row in column2]

        # Combine both lists to cover duplicate realtionships
        return friendships_column1 + friendships_column2


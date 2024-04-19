'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from models import * 
from models import FriendRequest
from pathlib import Path

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
def insert_user(username: str, password: str):
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)

<<<<<<< HEAD
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
=======
def friendRequest(username: str, friend: str):
    with Session(engine) as session:
        request = FriendRequest(username,friend)
        session.add(request)
        session.commit()
>>>>>>> 650493faca13f9b30136316018c204b347763d08

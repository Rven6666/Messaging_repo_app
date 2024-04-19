'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import * 
# from models import FriendRequest
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

def friend_request(sender: str, receiver: str):
    with Session(engine) as session:
        request = FriendRequest(sender=sender, receiver=receiver)
        session.add(request)
        session.commit()

def cancel_request(sender: str, receiver: str):
    print('cancel fucntions')
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


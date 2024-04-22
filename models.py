'''
models
defines sql alchemy data models
also contains the definition for the room class used to keep track of socket.io rooms

Just a sidenote, using SQLAlchemy is a pain. If you want to go above and beyond, 
do this whole project in Node.js + Express and use Prisma instead, 
Prisma docs also looks so much better in comparison

or use SQLite, if you're not into fancy ORMs (but be mindful of Injection attacks :) )
'''

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
# modified import of 'declarative base'
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from typing import Dict
import encyrption 
import db


# data models

Base = declarative_base()


# model to store user information
class User(Base):
    __tablename__ = "user"

    # looks complicated but basically means
    # I want a username column of type string,
    # and I want this column to be my primary key
    # then accessing john.username -> will give me some data of type string
    # in other words we've mapped the username Python object property to an SQL column of type String
    
    username: Mapped[str] = Column(String, primary_key=True) 
    password: Mapped[str] = Column(String)
    is_conn: Mapped[bool] = Column(Boolean)
    # privateKey: Mapped[int] = mapped_column(Integer)



# stateful counter used to generate the room id
class Counter():
    def __init__(self):
        self.counter = 0

    def get(self):
        self.counter += 1
        return self.counter

# Room class, used to keep track of which username is in which room
class Room():
    def __init__(self):
        self.counter = Counter()
        # dictionary that maps the username to the room id
        # for example self.dict["John"] -> gives you the room id of
        # the room where John is in
        self.dict: Dict[str, int] = {}

    def create_room(self, sender: str, receiver: str) -> int:
        room_id = self.counter.get()
        self.dict[sender] = room_id
        self.dict[receiver] = room_id
        return room_id

    def join_room(self,  sender: str, room_id: int) -> int:
        self.dict[sender] = room_id

    def leave_room(self, user):
        if user not in self.dict.keys():
            return
        del self.dict[user]

    # gets the room id from a user
    def get_room_id(self, user: str):
        if user not in self.dict.keys():
            return None
        return self.dict[user]
    
class FriendRequest(Base):
    __tablename__ = "friend_requests"

    sender = Column(String, ForeignKey('user.username'), primary_key=True)
    receiver = Column(String, ForeignKey('user.username'), primary_key=True)


    # friend list table
class FriendList(Base):
    __tablename__ = "friend_list"

    friend1 = Column(String, ForeignKey('user.username'),primary_key=True)
    friend2 = Column(String, ForeignKey('user.username'),primary_key=True)
       
    # Makes sure each row is uniqure
    __table_args__ = (
        UniqueConstraint('friend1', 'friend2', name='unique_friend_row'),
    )

class publicKeys(Base):
    __tablename__ = "pubKeys"
    # sets up columns for pibkeys table
    publicKey = Column(Integer,  primary_key=True)
    GenKey = Column(Integer, primary_key=True)

        # Override __init__ method
    def __init__(self, publicKey, GKey):
        self.publicKey = publicKey
        self.GenKey = GKey

   
    



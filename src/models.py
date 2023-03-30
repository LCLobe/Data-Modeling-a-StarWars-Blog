import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column("id", Integer(), primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False) #Encript
    
    favourites = relationship("Favourites", back_populates="user")
    posts = relationship("Post", back_populates="owner")

class Favourites(Base):
    __tablename__ = 'favourite'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("user.id"))
    
    user = relationship("User", back_populates="user.favourites")
    post = relationship("Post", back_populates="post.favourites")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    owner_id = Column(Integer(), ForeignKey("user.id"))
    media_id = Column(Integer(), ForeignKey("user.id"))
    media_type = Column(Enum(), nullable=False)

    favourites = relationship("Favourites", back_populates="favourites.post")
    owner = relationship("User", back_populates="user.post")
    planet_media = relationship("Planet", back_populates="planet.post")
    character_media = relationship("Character", back_populates="character.post")



class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    terrain = Column(String(250), nullable=True)
    gravity = Column(String(250), nullable=True)
    radius = Column(String(250), nullable=True)

    born_here = relationship("Character", back_populates("character.planet"))
    post = relationship("Post", back_populates("post.planet_media"))

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=True)
    birthdate = Column(String(250), nullable=True)
    gender = Column(String(250), nullable=True)
    eye_color = Column(String(250), nullable=True)
    origin_planet = Column(String(250), ForeignKey("planet.id"))

    planet = relationship("Planet", back_populates("planet.born_here"))
    post = relationship("Post", back_populates("post.character_media"))
   
# class Media(Base):
#     __tablename__ = 'media'
#     id = Column(Integer(), primary_key=True)
#     type = Column(Enum(), nullable=False)
#     url = Column(String(250), nullable=False)
#     post_id = Column(Integer(), ForeignKey("post.id"))
#     post = relationship("Post", back_populates="media")

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e

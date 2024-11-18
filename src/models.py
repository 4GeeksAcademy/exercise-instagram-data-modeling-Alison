import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    posts = relationship("Post", back_populates="user")
    followers = relationship("Follower", foreign_keys="[Follower.user_to_id]")
    following = relationship("Follower", foreign_keys="[Follower.user_from_id]")

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String(250), nullable=False)

    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship("Post", back_populates="media")

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship("Post", back_populates="comments")

class Follower(Base):
    __tablename__ = 'follower'

    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

# Generar el diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Revisa el archivo diagram.png")
except Exception as e:
    print("Hubo un problema generando el diagrama")
    raise e

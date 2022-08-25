from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String, unique=True, index = True)
    password_hash = Column(String)
    is_active = Column(Boolean, default = True)

    posts = relationship("Post", back_populates="author")
    

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(Integer, index = True)
    post = Column(String, index = True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"))

    author = relationship("User", back_populates="posts")

class Votes(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index = True)
    used_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCASE"))
    post_id = Column(Integer, ForeignKey("posts.id" , ondelete = "CASCASE"))

class Follower(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCASE"))
    following_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCASE"))
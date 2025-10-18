from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title= Column(String, index=True)
    content =  Column(String, index=True)
    published = Column(Boolean, default=True)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    disabled = Column(Boolean, default=False)
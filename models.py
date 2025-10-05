from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title= Column(String, index=True)
    content =  Column(String, index=True)
    published = Column(Boolean, default=True)
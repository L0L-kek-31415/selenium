from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "Posts"
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    user = Column(String())
    subreddit = Column(String())
    comments = Column(String)
    upvoted = Column(String())
    vote = Column(String())
    time = Column(String())

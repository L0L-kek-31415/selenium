from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "reddit_posts"
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    user = Column(String())
    subreddit = Column(String())
    comments = Column(Integer())
    upvoted = Column(Integer())
    vote = Column(Integer())
    time = Column(String())

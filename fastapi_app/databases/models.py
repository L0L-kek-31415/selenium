import strawberry
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


@strawberry.type
class Post:
    title: str
    user: str
    subreddit: str
    comments: int
    upvoted: int
    vote: int
    time: str


Base = declarative_base()


class PostPostgres(Base):
    __tablename__ = "Posts"
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    user = Column(String())
    subreddit = Column(String())
    comments = Column(String)
    upvoted = Column(String())
    vote = Column(String())
    time = Column(String())

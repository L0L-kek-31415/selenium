from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from databases.base_class import BaseDBService
from databases.models import PostPostgres, Post, Base


load_dotenv(".env.postgres")


class PostgresService(BaseDBService):
    def __enter__(self):
        self.conn_url = (
            f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
            f'{os.getenv("POSTGRES_PASSWORD")}@'
            f'{os.getenv("POSTGRES_SERVER")}:{os.getenv("POSTGRES_PORT")}/'
            f'{os.getenv("POSTGRES_DB")}'
        )
        engine = create_engine(self.conn_url, pool_pre_ping=True)
        Base.metadata.create_all(engine)
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)
        self.db = self.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def return_all(self):
        result = []
        for post in self.db.query(PostPostgres).all():
            result.append(
                Post(
                    title=post.title,
                    user=post.user,
                    subreddit=post.subreddit,
                    comments=int(post.comments),
                    upvoted=int(post.upvoted),
                    vote=int(post.vote),
                    time=str(post.time),
                )
            )
        return result

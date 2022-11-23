from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from db.base_db_class import BaseDBService
from db.models_postgres import Post, Base

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

    def add_post(self, post):
        new_post = Post(
            title=post["title"],
            user=post["user"],
            subreddit=post["subreddit"],
            comments=int(post["comments"]),
            upvoted=int(post["upvoted"]),
            vote=int(post["vote"]),
            time=self.get_datetime(post["time"]),
        )
        self.db.add(new_post)
        self.db.commit()
        self.db.flush()

    @staticmethod
    def get_datetime(time_my):
        if time_my is not None:
            data = " ".join(time_my.split()[:6])
            data = datetime.strptime(data, "%a, %b %d, %Y, %I:%M:%S %p")
            return data
        return None

    def return_all(self):
        result = []
        for item in self.db.query(Post).all():
            result.append((item.title, item.user, item.vote))
        return result

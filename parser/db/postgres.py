from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from parser.db.models_postgres import Post, Base

load_dotenv("../../.env.postgres")


class PostgresService:
    def __init__(self):
        self.conn_url = (
            f'postgresql+psycopg2://{os.getenv("POSTGRES_USER", "postgres")}:'
            f'{os.getenv("POSTGRES_PASSWORD", "postgres")}@postgres:5432/'
            f'{os.getenv("POSTGRES_DB", "postgres")}'
        )
        self.engine = None
        self.session = None
        self.db = None

    def __enter__(self):
        self.engine = self.start()
        self.session = sessionmaker(bind=self.engine)
        self.db = self.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def start(self):
        engine = create_engine(self.conn_url)
        Base.metadata.create_all(engine)
        return engine

    def add_post(self, post):
        new_post = Post(
            title=post["title"],
            user=post["user"],
            subreddit=post["subreddit"],
            comments=post["comments"],
            upvoted=post["upvoted"],
            vote=post["vote"],
            time=post["time"],
        )
        self.db.add(new_post)

    def return_all(self):
        return self.db.query(Post).all()

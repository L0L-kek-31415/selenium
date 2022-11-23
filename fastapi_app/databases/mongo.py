from dotenv import load_dotenv
from pymongo import MongoClient
import os

from databases.base_class import BaseDBService
from databases.models import Post


load_dotenv(".env.mongodb")


class MongoService(BaseDBService):
    def __enter__(self):
        self.name = "reddit_posts"
        self.url = (
            f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:"
            f"{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongodb:27017/"
        )
        client = MongoClient(self.url)
        self.db_client = client[self.name]
        self.db = self.db_client["posts"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_client.client.close()

    def return_all(self):
        posts = self.db.find({})
        result = []
        for post in posts:
            result.append(
                Post(
                    title=post["title"],
                    user=post["user"],
                    subreddit=post["subreddit"],
                    comments=int(post["comments"]),
                    upvoted=int(post["upvoted"]),
                    vote=int(post["vote"]),
                    time=str(post["time"]),
                )
            )
        return result

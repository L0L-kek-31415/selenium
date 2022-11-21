from dotenv import load_dotenv
from pymongo import MongoClient
import os


load_dotenv(".env.mongodb")


class MongoService:
    def __init__(self):
        self.name = "reddit_posts"
        self.url = (
            f"mongodb://{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}:"
            f"{os.getenv('MONGO_INITDB_ROOT_USERNAME')}@mongodb:27017/"
        )

    def __enter__(self):
        self.db_client = self.get_db()
        self.db = self.db_client["posts"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_client.client.close()

    def get_db(self):
        client = MongoClient(self.url)
        return client[self.name]

    def add_post(self, post):
        self.db.insert_one(post)

    def return_all(self):
        return self.db.find()

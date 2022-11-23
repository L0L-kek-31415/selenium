import json

from databases.base_class import BaseDBService
from databases.models import Post


class TxtDB(BaseDBService):
    def __init__(self):
        self.file_name = "/data/db.txt"

    def __enter__(self):
        self.file = open(self.file_name, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def return_all(self):
        self.file.seek(0)
        result = []
        for line in self.file:

            post = json.loads(line)
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

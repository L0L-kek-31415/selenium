import psycopg2
from dotenv import load_dotenv
import os

from parser.db.base_db_class import BaseDBService

load_dotenv(".env.postgres")


class PostgresService(BaseDBService):
    def __enter__(self):
        db = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_DB")
        self.conn = psycopg2.connect(
            database=db,
            user=user,
            password=password,
            host="postgres",
            port="5432",
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS reddit ("
            "id serial primary key,"
            " title varchar,"
            " owner varchar,"
            " subreddit varchar,"
            " comments integer,"
            " upvoted integer,"
            " vote integer,"
            " time_my varchar);"
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        self.cur.close()

    def add_post(self, post):
        self.cur.execute(
            "INSERT INTO reddit (title, owner, subreddit,"
            " comments, upvoted, vote, time_my) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (
                post["title"],
                post["user"],
                post["subreddit"],
                int(post["comments"]),
                int(post["upvoted"]),
                int(post["vote"]),
                post["time"],
            ),
        )
        self.conn.commit()

    def return_all(self):
        result = []
        self.cur.execute("select * from reddit")
        rows = self.cur.fetchall()
        for i in rows:
            result.append(i)
        return result

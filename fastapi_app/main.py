from typing import List
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from databases.models import Post
from databases.mongo import MongoService
from databases.postgres import PostgresService
from databases.txt_db import TxtDB


@strawberry.type
class Query:
    @strawberry.field
    def all_posts(self) -> List[Post]:
        result = []
        with MongoService() as mongo:
            result += mongo.return_all()
        with PostgresService() as postgres:
            result += postgres.return_all()
        with TxtDB() as file_db:
            result += file_db.return_all()
        return result

    @strawberry.field
    def mongo_posts(self) -> List[Post]:
        with MongoService() as mongo:
            return mongo.return_all()

    @strawberry.field
    def postgres_posts(self) -> List[Post]:
        with PostgresService() as postgres:
            return postgres.return_all()

    @strawberry.field
    def txt_posts(self) -> List[Post]:
        with TxtDB() as file_db:
            return file_db.return_all()


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

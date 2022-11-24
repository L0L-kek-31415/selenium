from parser.rabbit.consumer import BaseConsumer
from parser.subreddit_parser.subredditService import SubredditService


class Consumer(BaseConsumer):
    def __init__(self, workers, queue="syka"):
        super().__init__(workers, queue)

    def callback(self, ch, method, properties, body):
        param = body.decode("utf-8")
        self.pool.apply_async(SubredditService, (param,))

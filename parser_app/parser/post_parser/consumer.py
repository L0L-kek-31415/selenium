from parser.post_parser.worker import Worker
from parser.rabbit.consumer import BaseConsumer


class Consumer(BaseConsumer):
    def __init__(self, workers, queue="link"):
        super().__init__(workers, queue)

    def callback(self, ch, method, properties, body):
        param = body.decode("utf-8")
        self.pool.apply_async(Worker, (param,))

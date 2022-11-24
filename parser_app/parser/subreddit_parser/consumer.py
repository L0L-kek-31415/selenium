import multiprocessing
import pika

from parser.subreddit_parser.subredditService import SubredditService


class Consumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit")
        )
        self.channel = self.connection.channel()
        self.pool = multiprocessing.Pool(5)
        self.queue = self.channel.queue_declare("syka")
        self.channel.basic_consume(
            queue="syka",
            on_message_callback=self.callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def consume(self):
        pass

    def callback(self, ch, method, properties, body):
        param = body.decode("utf-8")
        self.pool.apply_async(SubredditService, (param,))

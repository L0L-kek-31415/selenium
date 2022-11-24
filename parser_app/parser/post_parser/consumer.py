import multiprocessing

import pika

from parser.post_parser.worker import Worker


class Consumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit")
        )
        self.channel = self.connection.channel()
        self.pool = multiprocessing.Pool(5)
        self.queue = self.channel.queue_declare("link")
        self.channel.basic_consume(
            queue="link",
            on_message_callback=self.callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def consume(self):
        pass

    def callback(self, ch, method, properties, body):
        print("consumer get link ", body)
        param = body.decode("utf-8")
        print(param)
        self.pool.apply_async(Worker, (param,))

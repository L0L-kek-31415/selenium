import multiprocessing
import pika


class BaseConsumer:
    def __init__(self, workers, queue):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit")
        )
        self.channel = self.connection.channel()
        self.pool = multiprocessing.Pool(workers)
        self.queue = self.channel.queue_declare(queue)
        self.channel.basic_consume(
            queue=queue,
            on_message_callback=self.callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        pass

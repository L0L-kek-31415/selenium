import pika


class BaseProducer:
    def __init__(self, queue):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit", port=5672)
        )
        self.queue_name = queue
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue)

    def publish(self, body):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=body,
        )

    def close(self):
        self.channel.close()
        self.connection.close()

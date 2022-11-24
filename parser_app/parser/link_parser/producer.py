import pika


class Producer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit", port=5672)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare("link")

    def publish(self, body):
        self.channel.basic_publish(exchange="", routing_key="link", body=body)

    def close(self):
        self.channel.close()
        self.connection.close()

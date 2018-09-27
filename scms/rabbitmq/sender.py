"""
Using for sending message to the rabbit server in COCS
and the client of COCS can recieve the message.
"""

import pika
from scms.common import exceptions
from scms.rabbitmq import connection


class Sender(object):

    def generate_message(self, action, param_dict):
        if action is None:
            raise exceptions.ParamMissing("action")

        message = {"Action": action, "Params": param_dict}
        # message = json.dumps(message)
        return message

    def send_message(exchange_name, routing_key, message):
        client = connection.get_rabbitmq_client()
        print(client)
        channel = client.channel()
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type='topic')

        channel.basic_publish(exchange=exchange_name,
                              routing_key=routing_key,
                              body=message)
        print(" [x] Sent %r:%r" % (routing_key, message))
        client.close()
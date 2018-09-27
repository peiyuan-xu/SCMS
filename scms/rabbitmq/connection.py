"""
Connection to RabbitMQ server management
"""
import threading

from pyrabbit.api import Client

from scms.common.exceptions import RabbitMQClientDead

_LOCK = threading.Lock()
RABBITMQ_CLIENT = None


def _init_client():
    # whether multi client is better or not
    global _LOCK
    with _LOCK:
        global RABBITMQ_CLIENT
        if not RABBITMQ_CLIENT or not RABBITMQ_CLIENT.is_alive():
            RABBITMQ_CLIENT = Client('localhost:15672', 'guest', 'guest')


def get_rabbitmq_client():
    global RABBITMQ_CLIENT
    if not RABBITMQ_CLIENT or not RABBITMQ_CLIENT.is_alive():
        _init_client()

    if not RABBITMQ_CLIENT.is_alive():
        raise RabbitMQClientDead()
    return RABBITMQ_CLIENT

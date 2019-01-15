#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc: Connection to RabbitMQ server management
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
        if not RABBITMQ_CLIENT:
            RABBITMQ_CLIENT = Client('192.168.1.220:15672', 'scms', 'scms')


def get_rabbitmq_client():
    global RABBITMQ_CLIENT
    if not RABBITMQ_CLIENT:
        _init_client()

    return RABBITMQ_CLIENT

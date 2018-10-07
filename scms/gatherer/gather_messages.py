#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 20:34
@desc:
"""

from scms.common import constants
from scms.gatherer import connection as conn


class GatherMessages:
    queues_mess_count_dict = {}

    def __init__(self):
        self.rabbit_client = conn.get_rabbitmq_client()

    def get_message_count_in_queues(self):
        queues = self.rabbit_client.get_queues(vhost=constants.RABBITMQ_VHOST)
        for queue in queues:
            depth = queue['messages']
            GatherMessages.queues_mess_count_dict[queue['name']] = depth

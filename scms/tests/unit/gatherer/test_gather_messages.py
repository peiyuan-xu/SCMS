#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/6 20:37
@desc:
"""

import time
import unittest

from scms.common import constants as con
from scms.scheduler import connection as conn
from scms.scheduler.gather_messages import GatherMessages
from scms.tests.base import BaseTestCase


class GatherMessagesTest(BaseTestCase):

    def setUp(self):
        # create vhost
        client = conn.get_rabbitmq_client()
        client.create_vhost(con.RABBITMQ_VHOST)
        client.set_vhost_permissions(con.RABBITMQ_VHOST, 'guest', '.*', '.*', '.*')
        client.create_exchange(con.RABBITMQ_VHOST, 'test_exchange', 'direct')
        pass

    def tearDown(self):
        pass

    def test_gather_message_count_in_queue(self):
        client = conn.get_rabbitmq_client()
        # create queue
        client.create_queue(con.RABBITMQ_VHOST, 'serviceA_chain1')
        # create binding
        client.create_binding(con.RABBITMQ_VHOST, 'test_exchange', 'serviceA_chain1', 'my.rtkey')
        # add messages
        message = "hello-message1"
        if client.is_alive:
            print("connection alive")
        else:
            print("conn dead")
        client.publish(vhost=con.RABBITMQ_VHOST, xname='test_exchange', rt_key='my.rtkey', payload=message)
        message = "hello- message2"
        client.publish(vhost=con.RABBITMQ_VHOST, xname='test_exchange', rt_key='my.rtkey', payload=message)

        # test getting message's count using gatherer
        time.sleep(5)
        gather_message = GatherMessages()
        gather_message.get_message_count_in_queues()
        self.assertEqual(GatherMessages.queues_mess_count_dict['queue1'], 2)


if __name__ == '__main__':
    unittest.main()

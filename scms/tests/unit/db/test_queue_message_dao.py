#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc:
"""

import time

from scms.db.api import ChainDao
from scms.db.api import ServiceDao
from scms.db.api import QueueMessageDao
from scms.db import common
from scms.db.models import ModelBase
from scms.tests.base import BaseTestCase
import unittest


class QueueMessageDAOTest(BaseTestCase):

    def setUp(self):
        ModelBase.metadata.create_all(common.get_engine())

    def tearDown(self):
        # close the session connected to the mysql
        common.get_session().close()
        ModelBase.metadata.drop_all(common.get_engine())
        pass

    def test_add_queue_message(self):
        chain1 = {'name': "chain1"}
        chain2 = {'name': "chain2"}
        chain_dao = ChainDao()
        chain_dao.create_chain(chain1)
        chain_dao.create_chain(chain2)

        serviceA = {'name': "serviceA"}
        serviceB = {'name': "serviceB"}
        service_dao = ServiceDao()
        service_dao.create_service(serviceA)
        service_dao.create_service(serviceB)

        # create queuemessage
        queue_messaage_dao = QueueMessageDao()
        queue_messaage_dao.create_queue_message("serviceA", "chain1", 100)
        queue_messaage_dao.create_queue_message("serviceB", "chain1", 20)
        queue_messaage_dao.create_queue_message("serviceA", "chain2", 800)
        time.sleep(1)
        queue_messaage_dao.create_queue_message("serviceA", "chain1", 300)

        message_num_list = queue_messaage_dao.list_message_by_chain_and_service(
            "serviceA", "chain1"
        )
        self.assertEqual(2, len(message_num_list))
        self.assertEqual(300, message_num_list[0]['message_number'])


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc:
"""

from scms.db.api import ChainDao
from scms.db.api import ServiceDao
from scms.db.api import ChainWithServiceDAO
from scms.db import common
from scms.db.models import ModelBase, ChainWithService
from scms.tests.base import BaseTestCase
import unittest


class QueueWithServiceDAOTest(BaseTestCase):

    def setUp(self):
        ModelBase.metadata.create_all(common.get_engine())

    def tearDown(self):
        # close the session connected to the mysql
        common.get_session().close()
        ModelBase.metadata.drop_all(common.get_engine())
        pass

    def test_queue_with_service(self):
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

        # create chain with service
        chain_with_service_dao = ChainWithServiceDAO()
        chain_with_service_dao.create_chain_with_service("chain1", "serviceA")
        chain_with_service_dao.create_chain_with_service("chain1", 'serviceB')
        chain_with_service_dao.create_chain_with_service('chain2', 'serviceA')

        c_with_s_list = chain_with_service_dao.paginate_list_resource(ChainWithService, 0)
        self.assertEqual(c_with_s_list.count(), 3)
        c_with_s_temp = chain_with_service_dao.get_chain_with_service('chain2', 'serviceB')
        self.assertEqual(c_with_s_temp, None)
        c_with_s_temp = chain_with_service_dao.get_chain_with_service('chain1', 'serviceA')
        self.assertEqual(c_with_s_temp['chain']['name'], 'chain1')
        self.assertEqual(c_with_s_temp['service']['name'], 'serviceA')


if __name__ == '__main__':
    unittest.main()

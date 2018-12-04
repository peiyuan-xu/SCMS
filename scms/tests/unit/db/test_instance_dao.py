#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/4 20:53
@desc:
"""
from scms.db.api import ChainDao
from scms.db.api import ImageDAO
from scms.db.api import InstanceDAO
from scms.db.api import ServiceDao
from scms.db import common
from scms.db.models import ModelBase
from scms.tests.base import BaseTestCase


class InstanceDAOTest(BaseTestCase):
    def setUp(self):
        ModelBase.metadata.create_all(common.get_engine())

    def tearDown(self):
        # close the session connected to the mysql
        common.get_session().close()
        ModelBase.metadata.drop_all(common.get_engine())
        pass

    def test_create_instance(self):
        chain1 = {'name': "chain1"}
        chain_dao = ChainDao()
        chain_dao.create_chain(chain1)

        serviceA = {'name': "serviceA"}
        service_dao = ServiceDao()
        service_dao.create_service(serviceA)

        image_dao = ImageDAO()
        image_name = "image_v1"
        image = image_dao.create_image("serviceA", image_name, True)

        container_id = 'container_2018120401'
        container_dao = InstanceDAO()
        container_dao.create_instance("serviceA", image['id'], "chain1", container_id)
        container_id = 'container_2018120402'
        container_dao.create_instance("serviceA", image['id'], "chain1", container_id)

        res_list = container_dao.list_instance_by_service_and_chain("serviceA", "chain1")
        self.assertEqual(2, len(res_list))

        container_dao.delete_instance_by_instanceid(container_id)
        res_list = container_dao.list_instance_by_service_and_chain("serviceA", "chain1")
        self.assertEqual(1, len(res_list))

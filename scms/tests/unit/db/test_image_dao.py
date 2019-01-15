#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/4 20:03
@desc:
"""
from scms.db.api import ImageDAO
from scms.db.api import ServiceDao
from scms.db import common
from scms.db.models import ModelBase
from scms.tests.base import BaseTestCase


class ImageDAOTest(BaseTestCase):
    def setUp(self):
        ModelBase.metadata.create_all(common.get_engine())

    def tearDown(self):
        # close the session connected to the mysql
        common.get_session().close()
        ModelBase.metadata.drop_all(common.get_engine())
        pass

    def test_create_image(self):
        serviceA = {'name': "serviceA"}
        serviceB = {'name': "serviceB"}
        service_dao = ServiceDao()
        service_dao.create_service(serviceA)
        service_dao.create_service(serviceB)

        # create image
        image_dao = ImageDAO()
        image_name = "image_v1"
        image_dao.create_image("serviceA", image_name)

        image_name = "image_v2"
        command = ''
        image_dao.create_image("serviceA", image_name, command, True)

        res = image_dao.get_image_by_name(image_name)
        self.assertTrue(res['last'])
        res_list = image_dao.list_images_by_service("serviceA")
        self.assertEqual(2, len(res_list))


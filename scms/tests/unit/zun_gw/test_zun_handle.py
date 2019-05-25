#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/11/17 15:23
@desc:
"""
import time

import unittest

from scms.tests.base import BaseTestCase
from scms.zun_gw.zun_handle import ZunHandle


class ZunHandleTest(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_list_containers(self):
        # before test list_containers, I have created
        # a container named 'test_name_1' in the server of zun
        zun_handle = ZunHandle()
        f = {}
        res = zun_handle.list_containers(f)
        print(res)
        self.assertEqual(len(res), 1)

        f = {'name': 'test_name_1'}
        res = zun_handle.list_containers(f)
        print(res)
        self.assertEqual(len(res), 1)

        # f = {'name': 'test_name'}
        # res = zun_handle.list_containers(f)
        # self.assertRaises()

    def test_get_container(self):
        # before test list_containers, I have created
        # a container named 'test_name_1' in the server of zun
        resource_id = 'b036b6f9-c3f6-464a-919a-f372963adf12'
        zun_handle = ZunHandle()
        res = zun_handle.get_container(resource_id)
        self.assertEqual(res['uuid'], resource_id)

    def test_create_container(self):
        name = 'test_name_2'
        image = 'lymanxu/scms-servicedemo:v4'
        # using array for command
        command = ['ping', '8.8.8.8']

        zun_handle = ZunHandle()
        res = zun_handle.create_container(name=name,
                                          image=image,
                                          command=command)
        print(res)
        f = {'name': name}
        ress = zun_handle.list_containers(f)
        self.assertEqual(ress[0]['name'], name)

    def test_create_and_start_container(self):
        name = 'test_name_0524_3'
        image = 'scmsservice'
        # using array for command
        command = ['ping', '8.8.8.8']

        zun_handle = ZunHandle()
        res = zun_handle.create_and_start_container(name=name,
                                                    image=image,
                                                    command=command)
        print(res)
        f = {'name': name}
        ress = zun_handle.list_containers(f)
        print(ress)
        self.assertEqual(ress[0]['name'], name)
        self.assertEqual(res[0]['status'], 'Running')

    def test_delete_container(self):
        name = 'test_name_3'
        image = 'cirros'
        command = 'ping -c 4 8.8.8.8'

        zun_handle = ZunHandle()
        res = zun_handle.create_container(name=name,
                                          image=image,
                                          command=command)
        time.sleep(7)
        id = res['uuid']
        zun_handle.delete_container(id)
        time.sleep(7)
        f = {'name': name}
        res = zun_handle.list_containers(f)
        self.assertFalse(res)


if __name__ == '__main__':
    unittest.main()

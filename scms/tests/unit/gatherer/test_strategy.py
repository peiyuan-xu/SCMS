#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2019/1/15 13:07
@desc:
"""
import time
import unittest

from scms.gatherer.strategy import auto_add_container
from scms.gatherer.strategy import forecast
from scms.tests.base import BaseTestCase


class StrategyTest(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_forecast(self):
        raw_data_list = [1, 1, 3, 2, 3, 4, 5]
        resu = forecast(raw_data_list)
        self.assertTrue(resu)

    def test_auto_add_container(self):
        # the data exists
        chain = 'chain1'
        service = 'books'
        auto_add_container(chain, service)


if __name__ == '__main__':
    unittest.main()

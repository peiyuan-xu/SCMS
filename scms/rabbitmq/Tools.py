# !/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc:
"""

from pyrabbit.api import Client
cl = Client('localhost:55672', 'guest', 'guest')
cl.is_alive()
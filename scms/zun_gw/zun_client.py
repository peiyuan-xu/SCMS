#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/11/14 15:59
@desc: api for control containers through zunclient
"""

from zunclient import client as z_client


class ZunClient:

    zun_client = None

    @staticmethod
    def init_client():
        if ZunClient.zun_client is None:
            ZunClient.zun_client = ZunClient.get_client()

    @staticmethod
    def get_client():
        endpointurl = r'http://192.168.56.114/container/v1'

        client = z_client.Client(
            '1.2', auth_url='http://192.168.56.114/identity/v3',
            password='password',
            project_domain_id='default',
            project_domain_name='Default',
            project_name='admin',
            user_domain_id='default',
            user_domain_name='Default',
            username='admin',
            auth_type='password',
            endpoint_override=endpointurl)
        return client


ZunClient.init_client()

#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/11/15 10:51
@desc:
"""
from requests import exceptions as r_exceptions

from scms.common import exceptions as c_excp
from scms.zun_gw.zun_client import ZunClient


class ZunHandle:
    resource = 'containers'

    def __init__(self):
        self.client = ZunClient.zun_client
        if not self.client:
            self.client = ZunClient.get_client()

    def list_containers(self, filters):
        try:
            return [res.to_dict() for res in getattr(
                self.client, ZunHandle.resource).list(**filters)]
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable(service='zun',
                                              url=self.client.client.management_url)

    def create_container(self, *args, **kwargs):
        try:
            return getattr(self.client, ZunHandle.resource).create(
                *args, **kwargs
            ).to_dict()
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

    def get_container(self, resource_id):
        try:
            return getattr(self.client, ZunHandle.resource).get(
                resource_id).to_dict()
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

    def delete_container(self, resource_id):
        try:
            return getattr(self.client, ZunHandle.resource).delete(resource_id)
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

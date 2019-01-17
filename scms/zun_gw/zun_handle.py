#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/11/15 10:51
@desc:
"""
import time

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

    def start_container(self, id):
        try:
            return getattr(self.client, ZunHandle.resource).start(id)
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

    def create_and_start_container(self, *args, **kwargs):
        container = self.create_container(*args, **kwargs)
        while 'Creating' == container.get('status'):
            time.sleep(2)
            container = self.get_container(container['uuid'])

        self.start_container(container['uuid'])
        container = self.get_container(container['uuid'])
        return container

    def get_container(self, resource_id):
        try:
            return getattr(self.client, ZunHandle.resource).get(
                resource_id).to_dict()
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

    def stop_container(self, resource_id, timeout=0):
        try:
            return getattr(self.client, ZunHandle.resource).stop(resource_id, timeout)
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

    def delete_container(self, resource_id):
        try:
            return getattr(self.client, ZunHandle.resource).delete(resource_id)
        except r_exceptions.ConnectTimeout:
            raise c_excp.EndpointNotAvailable('zun',
                                              self.client.client.management_url)

    def stop_and_delete_container(self, resource_id):
        # resource_id is uuid
        self.stop_container(resource_id)
        container = self.get_container(resource_id)
        while 'Running' == container.get('status'):
            time.sleep(2)
            container = self.get_container(container['uuid'])

        return self.delete_container(container['uuid'])

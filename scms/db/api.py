#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc:
"""

import datetime

from sqlalchemy.exc import IntegrityError

from scms.common import exceptions
from scms.db.basedao import BaseDAO
from scms.db import models


class ChainDao(BaseDAO):

    def create_chain(self, chain_dict):
        if not chain_dict.get('name'):
            raise exceptions.ParamMissing('name')

        try:
            res = self.create_resource(models.Chain, chain_dict)
        except IntegrityError:
            raise exceptions.ResourceExist(models.Chain,
                                           chain_dict.get('name'))

        return res

    def delete_chain(self, chain_name):
        try:
            result = self.get_chain_by_name(chain_name)
            if not result:
                return

            self.delete_resource(models.Chain, result['id'])
        except Exception as e:
            raise exceptions.ResourceInUsing(models.Chain,
                                             chain_name, e)

    def update_chain(self, chain_name, update_dict):
        resu = self.get_chain_by_name(chain_name)
        if not resu:
            return

        return self.update_resource(models.Chain, resu['id'], update_dict)

    def get_chain_by_id(self, chain_id):
        return self.get_resource(models.Chain, chain_id)

    def get_chain_by_name(self, chain_name):
        filter_dict = {'name': chain_name}
        return self.get_resource_by_attr(models.Chain, filter_dict)

    def list_chain_by_attr(self, filter_dict):
        return self.list_resources_by_attr(models.Chain, filter_dict)


class ServiceDao(BaseDAO):

    def get_service_by_id(self, service_id):
        return self.get_resource(models.Service, service_id)

    def get_service_by_name(self, service_name):
        filter_dict = {'name': service_name}
        return self.get_resource_by_attr(models.Service, filter_dict)

    def create_service(self, service_dict):
        if not service_dict.get('name'):
            raise exceptions.ParamMissing('name')

        if self.get_service_by_name(service_dict['name']):
            return
        try:
            res = self.create_resource(models.Service, service_dict)
        except IntegrityError:
            raise exceptions.ResourceExist(models.Service,
                                           service_dict.get('name'))
        return res

    def delete_service(self, service_name):
        try:
            result = self.get_service_by_name(service_name)
            if not result:
                return

            self.delete_resource(models.Service, result['id'])
        except Exception as e:
            raise exceptions.ResourceInUsing(models.Chain,
                                             service_name, e)

    def update_service(self, service_name, update_dict):
        resu = self.get_service_by_name(service_name)
        if not resu:
            return

        return self.update_resource(models.Service, resu['id'], update_dict)

    def list_service_by_attr(self, filter_dict):
        return self.list_resources_by_attr(models.Service, filter_dict)


class QueueMessageDao(BaseDAO):

    def __init__(self):
        self.chain_dao = ChainDao()
        self.service_dao = ServiceDao()

    def get_queue_message_by_id(self, queue_message_id):
        return self.get_resource(models.QueueMessage, queue_message_id)

    def create_queue_message(self, service_name, chain_name, message_number):
        chain = self.chain_dao.get_chain_by_name(chain_name)
        if not chain:
            raise exceptions.ResourceNotFound(models.Chain, chain_name)

        service = self.service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)

        now_time = datetime.datetime.now()
        now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        queue_message_dict = {'chain_id': chain['id'], 'service_id': service['id'],
                              'message_number': message_number, 'timestamp': now_time}
        return self.create_resource(models.QueueMessage, queue_message_dict)

    def list_message_by_chain_and_service(self, service_name, chain_name):
        # select latest 100 rows
        chain = self.chain_dao.get_chain_by_name(chain_name)
        if not chain:
            raise exceptions.ResourceNotFound(models.Chain, chain_name)

        service = self.service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)

        dict = {'chain_id': chain['id'], 'service_id': service['id']}
        res_list = self.paginate_list_first_message_page(models.QueueMessage, dict)
        return res_list

    def list_message_by_chainid_and_serviceid(self, chain_id, service_id):
        dict = {'chain_id': chain_id, 'service_id': service_id}
        res_list = self.paginate_list_first_message_page(models.QueueMessage, dict)
        return res_list


class ChainWithServiceDAO(BaseDAO):

    def create_chain_with_service(self, chain_name, service_name, head=False):
        chian_dao = ChainDao()
        chain = chian_dao.get_chain_by_name(chain_name)
        if not chain:
            raise exceptions.ResourceNotFound(models.Chain, chain_name)
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)
        chain_with_service_dict = {'chain_id': chain['id'],
                                   'service_id': service['id'], 'head': head}
        return self.create_resource(models.ChainWithService, chain_with_service_dict)

    def delete_chain_with_service(self, chain_name, service_name):
        chian_dao = ChainDao()
        chain = chian_dao.get_chain_by_name(chain_name)
        if not chain:
            raise exceptions.ResourceNotFound(models.Chain, chain_name)
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)
        filter = {'chain_id': chain['id'], 'service_id': service['id']}

        res = self.get_resource_by_attr(models.ChainWithService, filter)
        if not res:
            raise exceptions.ResourceNotFound(models.ChainWithService, "")
        return self.delete_resource(models.ChainWithService, res['id'])

    def get_exit_with_chain_service(self, chain_name, service_name):
        chain_dao = ChainDao()
        chain = chain_dao.get_chain_by_name(chain_name)
        if not chain:
            return False
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            return False
        filter = {'chain_id': chain['id'], 'service_id': service['id']}
        resu = self.get_resource_by_attr(models.ChainWithService, filter)
        return resu


class ImageDAO(BaseDAO):
    def create_image(self, service_name, image_name, last=False):
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)
        dict = {'service_id': service['id'], 'image_name': image_name, 'last': last}
        try:
            res = self.create_resource(models.Image, dict)
        except IntegrityError:
            raise exceptions.ResourceExist(models.Image, image_name)
        return res

    def delete_image(self, image_name):
        filter = {'image_name': image_name}
        return self.delete_resource_by_attr(models.Image, filter)

    def get_image_by_name(self, image_name):
        filter = {'image_name': image_name}
        return self.get_resource_by_attr(models.Image, filter)

    def update_image_last(self, image_name, last):
        res = self.get_image_by_name(image_name)
        if not res:
            raise exceptions.ResourceNotFound(models.Image, image_name)
        dict = {'last': last}
        self.update_resource(models.Image, res['id'], dict)

    def list_images_by_service(self, service_name):
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)

        filter = {'service_id': service['id']}
        return self.list_resources_by_attr(models.Image, filter)


class InstanceDAO(BaseDAO):
    def create_instance(self, service_name, image_id, chain_name, container_id):
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)
        chain_dao = ChainDao()
        chain = chain_dao.get_chain_by_name(chain_name)
        if not chain:
            raise exceptions.ResourceNotFound(models.Service, chain_name)

        dict = {'service_id': service['id'], 'image_id': image_id,
                'chain_id': chain['id'], 'container_id': container_id}
        return self.create_resource(models.Instance, dict)

    def list_instance_by_service_and_chain(self, service_name, chain_name):
        service_dao = ServiceDao()
        service = service_dao.get_service_by_name(service_name)
        if not service:
            raise exceptions.ResourceNotFound(models.Service, service_name)
        chain_dao = ChainDao()
        chain = chain_dao.get_chain_by_name(chain_name)
        if not chain:
            raise exceptions.ResourceNotFound(models.Service, chain_name)

        filter = {'service_id': service['id'], 'chain_id': chain['id']}
        return self.list_resources_by_attr(models.Instance, filter)

    def list_instance_by_serviceid_and_chain_id(self, service_id, chain_id):
        filter = {'service_id': service_id, 'chain_id': chain_id}
        return self.list_resources_by_attr(models.Instance, filter)

    def delete_instance_by_instanceid(self, instance_id):
        filter = {'container_id': instance_id}
        # delete one, instace_id is unique
        return self.delete_resource_by_attr(models.Instance, filter)


#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/27 17:26
@desc:
"""

import pecan
from pecan import expose


from scms.common import exceptions
from scms.db.api import ServiceDao


class ServiceController(object):

    @expose(template='json')
    def post(self, **kw):
        if 'service' not in kw:
            pecan.abort(400, 'Request body service not found')
        service = kw['service']
        name = service.get('name', '').strip().encode("utf-8")
        # print('::' + name)
        # print('type:' + str(type(name)))
        if name == '':
            pecan.abort(400, "Request body service'name not found")

        service_dao = ServiceDao()
        try:
            service_dict = {'name': name}
            new_service = service_dao.create_service(service_dict)
        except exceptions.ResourceExist as e:
            print(e)
            pecan.abort(500, 'Failed to create service')
        return {'chain': new_service}

    @expose(template='json')
    def get(self, name):
        if name == '':
            pecan.abort(400, "Request body service'name not found")

        service_dao = ServiceDao()
        name = name.strip().encode('utf-8')
        service = service_dao.get_service_by_name(name)
        if not service:
            pecan.abort(404, 'Chain not found')
        return {'chain': service.to_dict()}

    @expose(template='json')
    def list(self):
        service_dao = ServiceDao()
        services_dict = service_dao.list_service_by_attr({})
        if not services_dict:
            pecan.abort(404, 'Service not found')
        return {'services': services_dict}

    @expose(template='json')
    def delete(self, name):
        if name == '':
            pecan.abort(400, "Request body service'name not found")

        name = name.strip().encode('utf-8')
        service_dao = ServiceDao()
        try:
            service_dao.delete_service(name)
        except exceptions.ResourceInUsing as e:
            print(e)
            pecan.abort(500, 'Failed to delete service')
        return {}

    @expose(template='json')
    def put(self):
        return "Using delete and create\n"

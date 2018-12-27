#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/27 20:39
@desc:
"""

import pecan
from pecan import expose


from scms.common import exceptions
from scms.db.api import ImageDAO


class ImageController(object):

    @expose(template='json')
    def post(self, **kw):
        if 'image' not in kw:
            pecan.abort(400, 'Request body image not found')
        image = kw['image']
        name = image.get('name', '').strip().encode("utf-8")
        service_name = image.get('service', '').strip().encode("utf-8")
        # print('::' + name)
        # print('type:' + str(type(name)))
        if name == '' or service_name == '':
            pecan.abort(400, "Request body image'name or service not found")

        last = False
        if 'last' in image:
            last = image.get('last').strip().encode('utf-8') == 'True'
        image_dao = ImageDAO()
        try:
            new_iamge = image_dao.create_image(service_name, name, last)
        except exceptions.ResourceExist as e:
            print(e)
            pecan.abort(500, 'Failed to create image')
        return {'chain': new_iamge}

    @expose(template='json')
    def get(self, name):
        if name == '':
            pecan.abort(400, "Request body image'name not found")

        image_dao = ImageDAO()
        name = name.strip().encode('utf-8')
        image = image_dao.get_image_by_name(name)
        if not image:
            pecan.abort(404, 'Image not found')
        return {'image': image.to_dict()}

    @expose(template='json')
    def list(self, **kw):
        image_dao = ImageDAO()

        if not kw or 'service' not in kw:
            images_dict = image_dao.list_images({})
            if not images_dict:
                pecan.abort(404, 'Image not found')
            return {'images': images_dict}
        elif not kw.get('service'):
            pecan.abort(400, "Request body image'name not found")
        else:
            service_name = kw.get('service').strip().encode('utf-8')
            try:
                images_dict = image_dao.list_images_by_service(service_name)
            except exceptions.ResourceNotFound:
                pecan.abort(404, 'Service not found')
            return {'images': images_dict}

    @expose(template='json')
    def delete(self, name):
        if name == '':
            pecan.abort(400, "Request body image'name not found")

        name = name.strip().encode('utf-8')
        image_dao = ImageDAO()
        try:
            image_dao.delete_image(name)
        except exceptions.ResourceInUsing as e:
            print(e)
            pecan.abort(500, 'Failed to delete image')
        return {}

    @expose(template='json')
    def put(self):
        return "Using delete and create\n"

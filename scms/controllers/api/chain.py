#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/25 16:18
@desc:
"""
import pecan
from pecan import expose


from scms.common import exceptions
from scms.db.api import ChainDao


class ChainController(object):

    @expose(template='json')
    def post(self, **kw):
        if 'chain' not in kw:
            pecan.abort(400, 'Request body chain not found')
        chain = kw['chain']
        name = chain.get('name', '').strip().encode("utf-8")
        # print('::' + name)
        # print('type:' + str(type(name)))
        if name == '':
            pecan.abort(400, "Request body chain'name not found")

        chain_dao = ChainDao()
        try:
            chain_dict = {'name': name}
            new_chain = chain_dao.create_chain(chain_dict)
        except exceptions.ResourceExist as e:
            print(e)
            pecan.abort(500, 'Failed to create chain')
        return {'chain': new_chain}

    @expose(template='json')
    def get(self, name):
        if name == '':
            pecan.abort(400, "Request body chain'name not found")

        chain_dao = ChainDao()
        name = name.strip().encode('utf-8')
        chain_dict = chain_dao.get_chain_by_name(name)
        if not chain_dict:
            pecan.abort(404, 'Chain not found')
        return {'chain': chain_dict}

    @expose(template='json')
    def list(self):
        chain_dao = ChainDao()
        chain_list = chain_dao.list_chain_by_attr({})
        if not chain_list:
            pecan.abort(404, 'Chain not found')
        return {'chains': chain_list}

    @expose(template='json')
    def delete(self, name):
        if name == '':
            pecan.abort(400, "Request body chain'name not found")

        name = name.strip().encode('utf-8')
        chain_dao = ChainDao()
        try:
            chain_dao.delete_chain(name)
        except exceptions.ResourceInUsing as e:
            print(e)
            pecan.abort(500, 'Failed to delete chain')
        return {}

    @expose(template='json')
    def put(self):
        return "Using delete and create\n"

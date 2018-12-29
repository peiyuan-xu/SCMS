#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/28 11:21
@desc:
"""

import pecan
from pecan import expose


from scms.common import exceptions
from scms.db.api import ChainWithServiceDAO


class ChainLinkController(object):

    @expose(template='json')
    def post(self, **kw):
        # create chain link list of a chain
        if 'chainlink' not in kw:
            pecan.abort(400, 'Request body chain link not found')
        chain_links = kw['chainlink']
        if 'chain' not in chain_links or not chain_links['chain']:
            pecan.abort(400, 'Request body chain not found')
        if 'link' not in chain_links or not chain_links['link']:
            pecan.abort(400, 'Request body link not found')

        chain_name = chain_links['chain'].strip().encode('utf-8')
        links_str = []
        for link in chain_links['link']:
            links_str.append(link.strip().encode("utf-8"))

        chain_link_dao = ChainWithServiceDAO()
        try:
            chain_link_dao.create_chain_link(chain_name, links_str)
        except exceptions.ResourceExist as e:
            print(e)
            pecan.abort(500, 'Failed to create chain links')
        return 'Success'

    @expose(template='json')
    def listlink(self, name):
        if name == '':
            pecan.abort(400, "Request body chain'name not found")

        name = name.strip().encode('utf-8')
        chain_link_dao = ChainWithServiceDAO()
        links = chain_link_dao.list_chain_link(name)
        return {name: links}


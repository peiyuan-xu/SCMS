#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/12/18 17:37
@desc:
"""
import pecan
from pecan import expose

from scms.db.api import ChainDao


class ChainController(object):
    @expose()
    def index(self):

        # chain_dao = ChainDao()
        # try:
        #     return {'pod': chain_dao.list_chain_by_attr({})}
        # except Exception as e:
        #     print(e)
        #     pecan.abort(500, _('Failed to list pods'))
        #     return
        return "Welcome to book section."

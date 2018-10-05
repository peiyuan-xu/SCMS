#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc: Using init db, this function will create tables automatically.
"""

from scms.db import common
from scms.db.models import ModelBase


def init_db():
    ModelBase.metadata.create_all(common.get_engine())


if __name__ == "__main__":
    init_db()

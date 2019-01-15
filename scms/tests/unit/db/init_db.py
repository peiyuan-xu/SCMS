#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2019/1/14 16:36
@desc:
"""
from scms.db.api import ChainDao
from scms.db.api import ChainWithServiceDAO
from scms.db.api import ImageDAO
from scms.db.api import ServiceDao
from scms.db import common
from scms.db.models import ModelBase
from scms.tests.base import BaseTestCase


class InitDB(BaseTestCase):

    def setUp(self):
        ModelBase.metadata.create_all(common.get_engine())

    def tearDown(self):
        # close the session connected to the mysql
        common.get_session().close()
        # ModelBase.metadata.drop_all(common.get_engine())
        pass

    def test_init_db(self):
        # create chains
        chain1 = {'name': "chain1"}
        chain2 = {'name': "chain2"}
        chain_dao = ChainDao()
        chain_dao.create_chain(chain1)
        chain_dao.create_chain(chain2)

        # create services
        books = {'name': "books"}
        reviews = {'name': "reviews"}
        score = {'name': "score"}
        service_dao = ServiceDao()
        service_dao.create_service(books)
        service_dao.create_service(reviews)
        service_dao.create_service(score)

        # create chain links
        chain_link_dao = ChainWithServiceDAO()
        chain_link_dao.create_chain_link('chain1', ['books', 'reviews', 'score'])

        chain_link = chain_link_dao.list_chain_link('chain1')
        chain_link_dao.create_chain_link('chain2', ['books', 'score'])

        # create images
        image_dao = ImageDAO()
        books_image = r'lymanxu/scms-servicedemo:v2'
        books_command = r'python SCMSServiceDemo/books.py'
        image_dao.create_image('books', books_image, books_command, True)

        reviews_image = r'lymanxu/scms-servicedemo:v2'
        reviews_command = r'python SCMSServiceDemo/reviews.py'
        image_dao.create_image('reviews', reviews_image, reviews_command, True)

        score_image = r'lymanxu/scms-servicedemo:v2'
        score_command = r'python SCMSServiceDemo/score.py'
        image_dao.create_image('score', score_image, score_command, True)

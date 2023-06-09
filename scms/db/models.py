#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/5 17:03
@desc:
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

ModelBase = declarative.declarative_base()

# QueueMessage Model
# refer http://docs.sqlalchemy.org/en/latest/orm/tutorial.html


class DictBase(object):
    attributes = []

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        d = {}
        for attr in self.__class__.attributes:
            d[attr] = getattr(self, attr)
        return d

    def __getitem__(self, key):
        return getattr(self, key)


class Chain(ModelBase, DictBase):
    __tablename__ = 'chain'
    attributes = ['id', 'name']
    id = Column('id', String(length=36), primary_key=True)
    name = Column('name', String(length=64), unique=True, nullable=False)
    # queuemessage = relationship("QueueMessage", backref="chain")
    chain_with_service = relationship("ChainWithService", backref="chain")


class Service(ModelBase, DictBase):
    __tablename__ = 'service'
    attributes = ['id', 'name']
    id = Column('id', String(length=36), primary_key=True)
    name = Column('name', String(length=64), unique=True, nullable=False)
    # queuemessage = relationship("QueueMessage", backref="service")
    chain_with_servie = relationship("ChainWithService", backref="service")


class QueueMessage(ModelBase, DictBase):
    __tablename__ = 'queuemessage'
    attributes = ['id', 'chain_id', 'service_id', 'message_number',
                  'timestamp']

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    chain_id = Column('chain_id', String(length=36), ForeignKey('chain.id'))
    service_id = Column('service_id', String(length=36), ForeignKey('service.id'))
    message_number = Column('message_number', Integer)
    timestamp = Column('timestamp',   TIMESTAMP,
                       server_default=text('CURRENT_TIMESTAMP'), index=True)


class ChainWithService(ModelBase, DictBase):
    __tablename__ = 'chainwithservice'
    attributes = ['id', 'chain_id', 'service_id', 'head', 'next_service_id']
    id = Column('id', String(length=36), primary_key=True)
    chain_id = Column('chain_id', String(length=36), ForeignKey('chain.id'))
    service_id = Column('service_id', String(length=36), ForeignKey('service.id'))
    head = Column('head', Boolean, default=False)
    next_service_id = Column('next_service_id', String(length=36))
    # chain = relationship("Chain", backref="chainwithservice")
    # service = relationship("Service", backref="chainwithservice")


class Image(ModelBase, DictBase):
    __tablename__ = 'image'
    attributes = ['id', 'service_id', 'image_name', 'command', 'last']
    id = Column('id', String(length=36), primary_key=True)
    service_id = Column('service_id', String(length=36), ForeignKey('service.id'))
    image_name = Column('image_name', String(length=36), nullable=False)
    command = Column('command', String(length=128))
    last = Column('last', Boolean, default=False)


class Instance(ModelBase, DictBase):
    __tablename__ = 'instance'
    attributes = ['id', 'service_id', 'image_id', 'chain_id', 'container_id']
    id = Column('id', String(length=36), primary_key=True)
    service_id = Column('service_id', String(length=36), ForeignKey('service.id'))
    image_id = Column('image_id', String(length=36), ForeignKey('image.id'))
    chain_id = Column('chain_id', String(length=36), ForeignKey('chain.id'))
    container_id = Column('container_id', String(64), unique=True, nullable=False)
    chain = relationship('Chain', backref="instances")
    service = relationship('Service', backref="instances")



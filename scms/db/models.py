from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
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
    queuemessage = relationship("QueueMessage", backref="chain")


class Service(ModelBase, DictBase):
    __tablename__ = 'service'
    attributes = ['id', 'name']
    id = Column('id', String(length=36), primary_key=True)
    name = Column('name', String(length=64), unique=True, nullable=False)
    queuemessage = relationship("QueueMessage", backref="service")


class QueueMessage(ModelBase, DictBase):
    __tablename__ = 'queuemessage'
    attributes = ['id', 'chain_id', 'service_id', 'message_number',
                  'timestamp']

    id = Column('id', String(length=36), primary_key=True)
    chain_id = Column('chain_id', String(length=36), ForeignKey('chain.id'))
    service_id = Column('service_id', String(length=36), ForeignKey('service.id'))
    message_number = Column('message_number', Integer)
    timestamp = Column('timestamp',   TIMESTAMP,
                       server_default=text('CURRENT_TIMESTAMP'), index=True)


class ChainWithService(ModelBase, DictBase):
    __tablename__ = 'chainwithservice'
    attributes = ['id', 'chain_id', 'service_id']
    id = Column('id', String(length=36), primary_key=True)
    chain_id = Column('chain_id', String(length=36), ForeignKey('chain.id'))
    service_id = Column('service_id', String(length=36), ForeignKey('service.id'))
    chain = relationship("Chain", backref="chainwithservice")
    service = relationship("Service", backref="chainwithservice")



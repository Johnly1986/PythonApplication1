# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Cache(Base):
    __tablename__ = 'cache'

    id = Column(Integer, primary_key=True)
    ip = Column(String(15))
    data = Column(String(256))
    time = Column(Integer)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    count = Column(Integer)
    location = Column(Integer)
    container = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    password = Column(String(10), nullable=False)

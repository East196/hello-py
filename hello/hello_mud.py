# -*- coding: utf-8 -*-

# 导入:
from sqlalchemy import Column, Integer, String, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20))
    defence = Column(Integer)
    rich = Column(Integer)
    king_id = Column(Integer)


class Hero(Base):
    __tablename__ = 'hero'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20))
    hp = Column(Integer)
    mp = Column(Integer)
    force = Column(Integer)
    intel = Column(Integer)
    city_id = Column(Integer)
    king_id = Column(Integer)


engine = create_engine('sqlite:///./hello.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add_all([
    City(name="ca", defence=1000, rich=1000),
    City(name="ly", defence=1000, rich=1000),
    City(name="yd", defence=1000, rich=1000),
    City(name="jy", defence=1000, rich=1000),
    City(name="xy", defence=1000, rich=1000),
    City(name="cd", defence=1000, rich=1000),
    Hero(name='tung', hp=100, mp=60, force=100, intel=60),
    Hero(name='cc', hp=100, mp=60, force=100, intel=60, city_id=3, king_id=2),
    Hero(name='lb', hp=100, mp=60, force=100, intel=60, city_id=6, king_id=3),
    Hero(name='sq', hp=100, mp=60, force=100, intel=60, city_id=4, king_id=4),
])

session.commit()
session.close()

heros = session.query(Hero).all()
print heros

# TODO use prettytable print details

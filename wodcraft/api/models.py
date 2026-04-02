# coding: utf-8
from sqlalchemy import (Column,
                        DateTime,
                        ForeignKey,
                        Index,
                        Integer,
                        SmallInteger,
                        Numeric,
                        String,
                        Enum,
                        Boolean,
                        UniqueConstraint,
                        Time,
                        Table, Date)
from sqlalchemy.orm import declarative_base, relationship, backref
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()
metadata = Base.metadata


ROLE_USER = 0
ROLE_ADMIN = 1

UNITS = dict([
    ('LB', 'Pounds'),
    ('KG', 'Killograms'),
    ('Pood', 'Pood')
])

SCORE_TYPES = dict([
    ('Rounds', 'Complete as many rounds as possible'),
    ('Reps', 'Complete as many repetitions as possible'),
    ('Weight', 'Lift as much weight as possible'),
    ('Time', 'Complete as fast as possible')
])


class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    name = Column(String(4), unique=True)
    description = Column(String(64))


class ScoreType(Base):
    __tablename__ = 'score_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    description = Column(String(64))


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    unit_id = Column(ForeignKey('unit.id'), index=False, nullable=True)
    score_type_id = Column(ForeignKey('score_type.id'), index=True)

    name = Column(String(256), unique=True)
    description = Column(String(4096), unique=True)
    weight = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    time = Column(DateTime, nullable=True)

    unit = relationship('Unit')
    score_type = relationship('ScoreType')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(128))  # salted and hashed
    role = Column(SmallInteger, default=ROLE_USER)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


tags = Table('tags',
             Base.metadata,
             Column('tag_id', Integer, ForeignKey('tag.id')),
             Column('score_id', Integer, ForeignKey('score.id')))


class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    activity_id = Column(ForeignKey('activity.id'), index=True)
    user_id = Column(ForeignKey('user.id'), index=True)

    when = Column(Date)
    weight = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    time = Column(Time, nullable=True)
    rx = Column(Boolean)
    comments = Column(String(256), nullable=True)
    tags = relationship('Tag',
                        secondary=tags,
                        backref=backref('score', lazy='dynamic'))

    user = relationship('User')
    activity = relationship('Activity')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    tag = Column(String(64))
    user = relationship('User')

    __table_args__ = (UniqueConstraint('user_id', 'tag'),)

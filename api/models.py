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
                        Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

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
    __searchable__ = ['name', 'description']

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
    nickname = Column(String(64), unique=True)
    email = Column(String(120), index=True, unique=True)
    role = Column(SmallInteger, default=ROLE_USER)


tags = Table('tags',
             Base.metadata,
             Column('tag_id', Integer, ForeignKey('tag.id')),
             Column('score_id', Integer, ForeignKey('score.id')))


class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    activity_id = Column(ForeignKey('activity.id'), index=True)
    user_id = Column(ForeignKey('user.id'), index=True)

    when = Column(DateTime)
    weight = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    time = Column(Time, nullable=True)
    rx = Column(Boolean)
    comments = Column(String(256), nullable=True)
    tags = relationship('Tag', secondary=tags, backref=backref('pages', lazy='dynamic'))

    user = relationship('User')
    activity = relationship('Activity')


class Tag(Base):
    __tablename__ = 'tag'
    __searchable__ = ['tag']
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    tag = Column(String(64))
    user = relationship('User')

    __table_args__ = (UniqueConstraint('user_id', 'tag'),)


#whooshalchemy.whoosh_index(app, Tag)


# class ComparableMixin:
#     def __eq__(self, other):
#         return not self < other and not other < self
#
#     def __ne__(self, other):
#         return self < other or other < self
#
#     def __gt__(self, other):
#         return other < self
#
#     def __ge__(self, other):
#         return not self < other
#
#     def __le__(self, other):
#         return not other < self


# class Score(Bases.Base, ComparableMixin):
#     activity = Bases.ForeignKey(Activity)
#     user = Bases.ForeignKey(User)
#     when = Bases.DateField(default=date.today, blank=False)
#     weight = Bases.IntegerField(null=True, blank=True)
#     unit = Bases.CharField(max_length=4,
#                             choices=UNITS,
#                             null=True,
#                             blank=True,
#                             default='LB')
#     reps = Bases.IntegerField(null=True, blank=True) # used for reps and rounds
#     time = Bases.TimeField(null=True, blank=True)
#     rx = Bases.BooleanField(default=True)
#     comments = Bases.TextField(max_length=1024, null=True, blank=True)
#     tags = Bases.ManyToManyField(Tag, null=True, blank=True)
#     activity_name = property(lambda self: self.activity.name)
#     activity_type = property(lambda self: self.activity.scoreType)
#
#     @property
#     def result(self):
#         t = self.activity_type
#         if t == 'Weight':
#             return str(self.weight) + ' ' + self.unit
#         elif t == 'Time':
#             return str(self.time)
#         elif t in ('Reps', 'Rounds'):
#             return str(self.reps)
#         else:
#             raise Exception('Unknown score type: ' + t)
#
#     def __lt__(self, other):
#         t = self.activity.scoreType
#         if t == 'Weight':
#             # Don't deal with unit conversions
#             assert self.unit == other.unit
#             return self.weight < other.weight
#         elif t == 'Time':
#             # A score is a lesser score if it took MORE time to complete
#             return self.time > other.time
#         elif t in ('Reps', 'Rounds'):
#             return self.reps < other.reps
#         else:
#             raise Exception('Unknown score type: ' + t)
#
#     def __unicode__(self):
#         a = self.activity
#         name = a.name
#         if self.activity_type == "Reps":
#             name = 'Max ' + name
#
#         return name + ' - ' + self.result
#
#     date_hierarchy = ['when']

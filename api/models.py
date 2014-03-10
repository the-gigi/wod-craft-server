# coding: utf-8
from datetime import datetime
from sqlalchemy.orm import relationship
from api import app
import flask.ext.whooshalchemy as whooshalchemy
from api import db


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


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), unique=True)
    description = db.Column(db.String(64))


class ScoreType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    description = db.Column(db.String(64))


class Activity(db.Model):
    __searchable__ = ['name', 'description']

    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.ForeignKey('unit.id'), index=False, nullable=True)
    score_type_id = db.Column(db.ForeignKey('score_type.id'), index=True)

    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(4096), unique=True)
    weight = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    time = db.Column(db.DateTime, nullable=True)

    unit = relationship('Unit')
    score_type = relationship('ScoreType')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    #about_me = db.Column(db.String(140), default='')
    #last_seen = db.Column(db.DateTime)
    # followed = db.relationship('User',
    #     secondary = followers,
    #     primaryjoin = (followers.c.follower_id == id),
    #     secondaryjoin = (followers.c.followed_id == id),
    #     backref = db.backref('followers', lazy = 'dynamic'),
    #     lazy = 'dynamic')

    # @staticmethod
    # def make_valid_nickname(nickname):
    #     return re.sub('[^a-zA-Z0-9_\.]', '', nickname)
    #
    # @staticmethod
    # def make_unique_nickname(nickname):
    #     if User.query.filter_by(nickname = nickname).first() == None:
    #         return nickname
    #     version = 2
    #     while True:
    #         new_nickname = nickname + str(version)
    #         if User.query.filter_by(nickname = new_nickname).first() == None:
    #             break
    #         version += 1
    #     return new_nickname
    #
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     return unicode(self.id)

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('score_id', db.Integer, db.ForeignKey('score.id'))
)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.ForeignKey('activity.id'), index=True)
    user_id = db.Column(db.ForeignKey('user.id'), index=True)
    unit_id = db.Column(db.ForeignKey('unit.id'), index=False, nullable=True)

    when = db.Column(db.DateTime)
    weight = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    time = db.Column(db.Time, nullable=True)
    rx = db.Column(db.Boolean)
    comments = db.Column(db.String(256), nullable=True)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('pages', lazy='dynamic'))

    user = relationship('User')
    activity = relationship('Activity')
    unit = relationship('Unit')


class Tag(db.Model):
    __searchable__ = ['tag']
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), index=True)
    tag = db.Column(db.String(64))
    user = relationship('User')

    __table_args__ = (db.UniqueConstraint('user_id', 'tag'),)


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


# class Score(models.Model, ComparableMixin):
#     activity = models.ForeignKey(Activity)
#     user = models.ForeignKey(User)
#     when = models.DateField(default=date.today, blank=False)
#     weight = models.IntegerField(null=True, blank=True)
#     unit = models.CharField(max_length=4,
#                             choices=UNITS,
#                             null=True,
#                             blank=True,
#                             default='LB')
#     reps = models.IntegerField(null=True, blank=True) # used for reps and rounds
#     time = models.TimeField(null=True, blank=True)
#     rx = models.BooleanField(default=True)
#     comments = models.TextField(max_length=1024, null=True, blank=True)
#     tags = models.ManyToManyField(Tag, null=True, blank=True)
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

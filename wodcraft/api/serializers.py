from marshmallow import Schema, fields


class UnitSerializer(Schema):
    name = fields.String()
    description = fields.String()


class ScoreTypeSerializer(Schema):
    name = fields.String()
    description = fields.String()


class ActivitySerializer(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    weight = fields.Integer(allow_none=True)
    reps = fields.Integer(allow_none=True)
    time = fields.DateTime(allow_none=True)
    score_type = fields.Nested(ScoreTypeSerializer)
    unit = fields.Nested(UnitSerializer)


class TagSerializer(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    tag = fields.String()


class ScoreSerializer(Schema):
    id = fields.Integer()
    activity = fields.Nested(ActivitySerializer)
    when = fields.Date(format='iso')
    weight = fields.Integer(allow_none=True)
    reps = fields.Integer(allow_none=True)
    time = fields.Time(allow_none=True)
    rx = fields.Boolean()
    comments = fields.String(allow_none=True)
    tags = fields.Nested(TagSerializer, many=True)


class UserSerializer(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    role = fields.Integer()

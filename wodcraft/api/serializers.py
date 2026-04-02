from marshmallow import Schema, fields


class UnitSerializer(Schema):
    name = fields.Str()
    description = fields.Str()


class ScoreTypeSerializer(Schema):
    name = fields.Str()
    description = fields.Str()


class ActivitySerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    weight = fields.Int(allow_none=True)
    reps = fields.Int(allow_none=True)
    time = fields.Raw(allow_none=True)
    score_type = fields.Nested(ScoreTypeSerializer)
    unit = fields.Nested(UnitSerializer, allow_none=True)


class TagSerializer(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tag = fields.Str()


class ScoreSerializer(Schema):
    id = fields.Int()
    activity = fields.Nested(ActivitySerializer)
    when = fields.Date(format='iso')
    weight = fields.Int(allow_none=True)
    reps = fields.Int(allow_none=True)
    time = fields.Raw(allow_none=True)
    rx = fields.Bool()
    comments = fields.Str(allow_none=True)
    tags = fields.Nested(TagSerializer, many=True)


class UserSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Int()

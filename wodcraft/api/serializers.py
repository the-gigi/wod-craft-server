from marshmallow import Schema, fields


class UnitSerializer(Schema):
    class Meta:
        fields = ('name', 'description')


class ScoreTypeSerializer(Schema):
    class Meta:
        fields = ('name', 'description')


class ActivitySerializer(Schema):
    score_type = fields.Nested(ScoreTypeSerializer)
    unit = fields.Nested(UnitSerializer)

    class Meta:
        fields = tuple('id name description weight reps time unit score_type'.split())


class TagSerializer(Schema):
    class Meta:
        fields = ('id', 'user_id', 'tag')


class ScoreSerializer(Schema):
    activity = fields.Nested(ActivitySerializer)
    tags = fields.Nested(TagSerializer, many=True)

    class Meta:
        fields = tuple('id activity when weight reps time rx comments tags'.split())
        dateformat = 'iso'


class UserSerializer(Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'role')

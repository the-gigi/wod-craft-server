from marshmallow import Serializer, fields


class UnitSerializer(Serializer):
    class Meta:
        fields = ('name', 'description')


class ScoreTypeSerializer(Serializer):
    class Meta:
        fields = ('name', 'description')


class ActivitySerializer(Serializer):
    score_type = fields.Nested(ScoreTypeSerializer)
    unit = fields.Nested(UnitSerializer)

    class Meta:
        fields = \
            'id name description weight reps time unit score_type'.split()


class TagSerializer(Serializer):
    class Meta:
        fields = 'id user_id tag'.split()


class ScoreSerializer(Serializer):
    activity = fields.Nested(ActivitySerializer)
    tags = fields.Nested(TagSerializer, many=True)

    class Meta:
        fields = 'id activity when weight reps time rx comments tags'.split()
        dateformat = 'iso'


class UserSerializer(Serializer):
    class Meta:
        fields = 'id name email role'.split()




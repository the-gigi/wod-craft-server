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
        fields = 'name description weight reps time unit score_type'.split()


class ScoreSerializer(Serializer):
    score_type = fields.Nested(ActivitySerializer)

    class Meta:
        fields = 'activity when weight reps time rx comments'.split()
        dateformat = 'iso'








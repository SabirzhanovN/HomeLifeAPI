from rest_framework import serializers
from .models import GradeDescription


class GradeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeDescription
        fields = ('id', 'description', 'category')
        read_only_fields = ('id',)

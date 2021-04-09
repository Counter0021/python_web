from rest_framework import serializers
from .models import Rubric


# Обработка рубрик
class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'name')

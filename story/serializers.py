from .models import *
from rest_framework import serializers


class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

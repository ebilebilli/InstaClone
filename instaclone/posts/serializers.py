from rest_framework import serializers
from .models import Post, Story

class PostSerializer(serializers.ModelSerializer):
    class meta:
        model = Post
        fields = '__all__'
        exlude = ['id']


class StorySerializer(serializers.ModelSerializer):
    class meta:
        model = Story
        fields = '__all__'
        exlude = ['id']
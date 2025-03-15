from rest_framework import serializers
from .models import Profile
from posts.serializers import *

class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    stories = StorySerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        exlude = ['id']
from rest_framework import serializers
from .models import Comment

class PostSerializer(serializers.ModelSerializer):
    class meta:
        model = Comment
        fields = '__all__'
        exlude = ['id']
from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class meta:
        model = Like
        fields = '__all__'
        exlude = ['id']
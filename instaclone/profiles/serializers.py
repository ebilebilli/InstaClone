from rest_framework import serializers
from .models import Profile

class PostSerializer(serializers.ModelSerializer):
    class meta:
        model = Profile
        fields = '__all__'
        exlude = ['id']
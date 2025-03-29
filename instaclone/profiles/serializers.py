from .models import Profile
from posts.serializers import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user:
           return user
        raise serializers.ValidationError('Invalid username or password')

class CustomerUserRegisterDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_two = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password_two'] 

    def validate(self, data):
        if data['password'] != data['password_two']:
            raise serializers.ValidationError({'password':['Passwords must match']})
        return data
            
    def create(self, validated_data):
        validated_data.pop('password_two')
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    stories = StorySerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['id']

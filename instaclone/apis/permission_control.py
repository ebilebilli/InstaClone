from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.permissions import BasePermission
from posts.models import Post, Story
from profiles.models import Profile
from comments.models import Comment

class HeHasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if isinstance(obj, Story):
            if obj.profile.profile_status == 'PRIVATE':
                if request.user != obj.profile.user and request.user not in obj.profile.followers.all():
                    return False
            if view.action in ['update', 'partial_update'] and request.user != obj.profile.user:
                return False
            return True

        if isinstance(obj, Profile):
            if obj.profile_status == 'PRIVATE':
                if request.user != obj.user and request.user not in obj.followers.all():
                    return False
            if view.action in ['update', 'partial_update'] and request.user != obj.user:
                return False
            return True

        if isinstance(obj, Post):
            if obj.profile.profile_status == 'PRIVATE':
                if request.user != obj.profile.user and request.user not in obj.profile.followers.all():
                    return False
            if view.action in ['update', 'partial_update'] and request.user != obj.profile.user:
                return False
            return True
        
        return False


class IsOwner(BasePermission):
    """
    Only the owner (creator) of the resource (Story, Post, Comment) can make requests.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the creator of the resource (owner of the resource)
        if isinstance(obj, Story):
            # Only the owner of the Story can make the request
            return obj.profile.user == request.user
        
        if isinstance(obj, Post):
            # Only the owner of the Post can make the request
            return obj.profile.user == request.user
        
        if isinstance(obj, Comment):
            # Only the owner of the Comment can make the request
            return obj.user == request.user
        
        return False

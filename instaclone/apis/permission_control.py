from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.authentication import TokenAuthentication


class HeHasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff
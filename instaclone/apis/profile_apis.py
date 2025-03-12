from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework.pagination import PageNumberPagination

from apis.permission_control import HeHasPermission, IsAuthenticated, AllowAny, TokenAuthentication
from posts.models import Post
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from posts.serializers import PostSerializer


class ProfilePagination(PageNumberPagination):
    page_size = 10  
    max_page_size = 100 


class ProfileSearchAPIView(APIView):
    pagination_class = ProfilePagination
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '')
        profiles = Profile.objects.filter(username__icontains=query) if query else Profile.objects.all()
        pagination = self.pagination_class
        if profiles.exists():
            result_page = pagination.paginate_queryset(profiles)
            serializer = ProfileSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There is not such user'}, status=status.HTTP_400_BAD_REQUEST)


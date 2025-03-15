from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework.pagination import PageNumberPagination

from apis.permission_control import HeHasPermission, IsAuthenticated, AllowAny, TokenAuthentication
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfilePagination(PageNumberPagination):
    """
    Pagination class for profiles.
    Sets the default page size to 10 and maximum page size to 100.
    """
    page_size = 10  
    max_page_size = 100 


class ProfileSearchAPIView(APIView):
    """
    API view to search profiles based on a query.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.

    Methods:
    - GET: Retrieves a list of profiles matching the search query.
    """
    pagination_class = ProfilePagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Search profiles by username.

        Args:
            request (Request): The search query in request parameters.

        Returns:
            - 200 OK: List of profiles matching the search query.
            - 400 Bad Request: If no profiles match the query or no query is provided.
        """
        query = request.query_params.get('query', '')
        profiles = Profile.objects.filter(username__icontains=query) if query else Profile.objects.all()
        pagination = self.pagination_class
        if profiles.exists():
            result_page = pagination.paginate_queryset(profiles)
            serializer = ProfileSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There is not such user'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailAPIView(APIView):
    """
    API view to retrieve, follow, or unfollow a specific profile.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    - HeHasPermission: Only users with permission can interact with the profile.

    Methods:
    - GET: Retrieves details of a specific profile.
    - POST: Follows a profile.
    - DELETE: Unfollows a profile.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, profile_id):
        """
        Retrieve details of a specific profile.

        Args:
            profile_id (int): ID of the profile to retrieve.

        Returns:
            - 200 OK: Profile data.
            - 403 Forbidden: If the user is not authorized to view the profile.
        """
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user == profile.user or profile.profile_status == Profile.OPEN_PROFILE or request.user in profile.followers.all():
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message':'You are not authorized to view this profile.'}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, profile_id):
        """
        Follow a specific profile.

        Args:
            profile_id (int): ID of the profile to follow.

        Returns:
            - 400 Bad Request: If the user tries to follow themselves or is already following.
            - 201 Created: If the user successfully follows the profile.
        """
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user == profile.user:
            return Response({'Message':'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        elif profile.followers.filter(id=request.user.id).exists():
            return Response({'Message':'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        profile.followers.add(request.user)
        profile.save()
        return Response({'Message':'Now, you are following this user'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, profile_id):
        """
        Unfollow a specific profile.

        Args:
            profile_id (int): ID of the profile to unfollow.

        Returns:
            - 400 Bad Request: If the user is not following the profile.
            - 200 OK: If the user successfully unfollows the profile.
        """
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        if not profile.followers.filter(id=request.user.id).exists():
            return Response({'Message':'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        profile.followers.remove(request.user)
        return Response({'Message':'You are no longer following this user'}, status=status.HTTP_200_OK)


class ProfileFollowerListAPIView(APIView):
    """
    API view to retrieve the list of followers for a specific profile.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.

    Methods:
    - GET: Retrieves a paginated list of followers for the profile.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = ProfilePagination

    def get(self, request, profile_id):
        """
        Retrieve a list of followers for a specific profile.

        Args:
            profile_id (int): ID of the profile whose followers are to be retrieved.

        Returns:
            - 200 OK: Paginated list of followers for the profile.
            - 403 Forbidden: If the user is not authorized to view the profile's followers.
        """
        profile = get_object_or_404(Profile, id=profile_id)
        pagination = self.pagination_class
        if request.user == profile.user or profile.profile_status == Profile.OPEN_PROFILE or request.user in profile.followers.all():
            followers = profile.followers.all()
            result_page = pagination.paginate_queryset(followers)
            serializer = ProfileSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer)
        return Response({'Message':'You are not authorized to view this profile.'}, status=status.HTTP_403_FORBIDDEN)


class ProfileFollowingListAPIView(APIView):
    """
    API view to retrieve the list of profiles a specific user is following.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.

    Methods:
    - GET: Retrieves a paginated list of profiles the user is following.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = ProfilePagination

    def get(self, request, profile_id):
        """
        Retrieve a list of profiles the user is following.

        Args:
            profile_id (int): ID of the profile whose followings are to be retrieved.

        Returns:
            - 200 OK: Paginated list of profiles the user is following.
            - 403 Forbidden: If the user is not authorized to view the profile's followings.
        """
        profile = get_object_or_404(Profile, id=profile_id)
        pagination = self.pagination_class
        if request.user == profile.user or profile.profile_status == Profile.OPEN_PROFILE or request.user in profile.followers.all():
            followings = profile.followings.all()
            result_page = pagination.paginate_queryset(followings)
            serializer = ProfileSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer)
        return Response({'Message':'You are not authorized to view this profile.'}, status=status.HTTP_403_FORBIDDEN)

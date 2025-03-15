from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from apis.permission_control import IsAuthenticated, TokenAuthentication, HeHasPermission, AllowAny, IsOwner
from posts.models import Story
from direct_messages.models import DirectMessage
from direct_messages.serializers import DirectMessageSerializer
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.serializers import StorySerializer


class OpenStoryListAPIView(APIView):
    """
    API view to retrieve a list of all publicly accessible stories.

    Permissions:
    - AllowAny: Any user, authenticated or not, can access this endpoint.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        """
        Retrieves all stories, ordered by creation date in descending order.

        Returns:
            Response:
                - 200 OK: A serialized list of stories.
                - 400 Bad Request: If no stories are available.
        """
        story = Story.objects.all().order_by('-created_at')
        if story.exists():
            serializer = StorySerializer(story, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no stories available.'}, status=status.HTTP_400_BAD_REQUEST)


class PrivateStoryListAPIView(APIView):
    """
    API view to retrieve a list of all stories with restricted access.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    - HeHasPermission: Additional custom permission is required.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request):
        """
        Retrieves all stories, ordered by creation date in descending order.

        Returns:
            Response:
                - 200 OK: A serialized list of stories.
                - 400 Bad Request: If no stories are available.
        """
        story = Story.objects.all().order_by('-created_at')
        if story.exists():
            serializer = StorySerializer(story, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no stories available.'}, status=status.HTTP_400_BAD_REQUEST)


class OpenStoryDetailAPIView(APIView):
    """
    API view to retrieve or delete a specific story.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    - AllowAny: Overrides IsAuthenticated, allowing any user to access (potential conflict).

    Methods:
    - GET: Retrieves details of a specific story.
    - DELETE: Deletes a specific story if the user is the owner.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, AllowAny]

    def get(self, request, story_id):
        """
        Retrieves the details of a specific story.

        Args:
            story_id (int): The ID of the story to retrieve.

        Returns:
            Response:
                - 200 OK: Serialized story data.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        serializer = StorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, story_id):
        """
        Deletes a specific story if the requesting user is the owner.

        Args:
            story_id (int): The ID of the story to delete.

        Returns:
            Response:
                - 204 No Content: If the story was deleted successfully.
                - 400 Bad Request: If the user is not authorized to delete the story.
        """
        story = get_object_or_404(Story, id=story_id)
        if story.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        story.delete()
        return Response({'message': 'Story deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class PrivateStoryDetailAPIView(APIView):
    """
    API view to retrieve or delete a specific story with restricted access.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    - HeHasPermission: Additional custom permission is required.

    Methods:
    - GET: Retrieves details of a specific story.
    - DELETE: Deletes a specific story if the user is the owner.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, story_id):
        """
        Retrieves the details of a specific story.

        Args:
            story_id (int): The ID of the story to retrieve.

        Returns:
            Response:
                - 200 OK: Serialized story data.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        serializer = StorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, story_id):
        """
        Deletes a specific story if the requesting user is the owner.

        Args:
            story_id (int): The ID of the story to delete.

        Returns:
            Response:
                - 204 No Content: If the story was deleted successfully.
                - 400 Bad Request: If the user is not authorized to delete the story.
        """
        story = get_object_or_404(Story, id=story_id)
        if story.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        story.delete()
        return Response({'message': 'Story deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class StoryCreateAPIView(APIView):
    """
    API view to create a new story.

    Permissions:
    - IsAuthenticated: Only authenticated users can create a story.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Creates a new story with the provided data.

        Args:
            request (Request): The request object containing story data.

        Returns:
            Response:
                - 201 Created: If the story was created successfully, with serialized data.
                - 400 Bad Request: If the provided data is invalid.
        """
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivateStoryLikeAPIView(APIView):
    """
    API view to like/unlike a story or retrieve its likes, with restricted access.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    - HeHasPermission: Additional custom permission is required.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, story_id):
        """
        Likes or unlikes a story based on the user's current like status.

        Args:
            story_id (int): The ID of the story to like or unlike.

        Returns:
            Response:
                - 200 OK: If the like was added or removed successfully.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        like_instance = Like.objects.filter(user=user, story=story).first()
        if like_instance:
            like_instance.delete()
            story.like_count = max(0, story.like_count - 1)
            story.save()
            return Response({'message': 'Like removed successfully.'}, status=status.HTTP_200_OK)

        Like.objects.create(user=user, story=story)
        story.like_count += 1
        story.save()
        return Response({'message': 'Story liked successfully.'}, status=status.HTTP_200_OK)

    def get(self, request, story_id):
        """
        Retrieves a list of likes for a specific story.

        Args:
            story_id (int): The ID of the story to retrieve likes for.

        Returns:
            Response:
                - 200 OK: A serialized list of likes if the user is authorized.
                - 403 Forbidden: If the user is not authorized to view the likes.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        if user == story.user or Like.objects.filter(user=user, story=story).exists():
            likes = Like.objects.filter(story=story)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'You are not authorized to view likes for this story.'}, status=status.HTTP_403_FORBIDDEN)


class OpenStoryLikeAPIView(APIView):
    """
    API view to like/unlike a story or retrieve its likes.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        """
        Likes or unlikes a story based on the user's current like status.

        Args:
            story_id (int): The ID of the story to like or unlike.

        Returns:
            Response:
                - 200 OK: If the like was added or removed successfully.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        like_instance = Like.objects.filter(user=user, story=story).first()
        if like_instance:
            like_instance.delete()
            story.like_count = max(0, story.like_count - 1)
            story.save()
            return Response({'message': 'Like removed successfully.'}, status=status.HTTP_200_OK)

        Like.objects.create(user=user, story=story)
        story.like_count += 1
        story.save()
        return Response({'message': 'Story liked successfully.'}, status=status.HTTP_200_OK)

    def get(self, request, story_id):
        """
        Retrieves a list of likes for a specific story.

        Args:
            story_id (int): The ID of the story to retrieve likes for.

        Returns:
            Response:
                - 200 OK: A serialized list of likes if the user is authorized.
                - 403 Forbidden: If the user is not authorized to view the likes.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        if user == story.user or Like.objects.filter(user=user, story=story).exists():
            likes = Like.objects.filter(story=story)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'You are not authorized to view likes for this story.'}, status=status.HTTP_403_FORBIDDEN)


class SendMessageToPrivateStoryAPIView(APIView):
    """
    API view to send a direct message to the owner of a private story.

    Permissions:
    - IsAuthenticated: Only authenticated users can send messages.
    - HeHasPermission: Additional custom permission is required.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, story_id):
        """
        Sends a direct message to the owner of a specific story.

        Args:
            story_id (int): The ID of the story whose owner will receive the message.
            request (Request): The request object containing message data.

        Returns:
            Response:
                - 201 Created: If the message was sent successfully, with serialized data.
                - 400 Bad Request: If the message data is invalid or missing.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        sender = request.user
        receiver = story.user

        chat = DirectMessage.objects.filter(sender_user=sender, receiver_user=receiver)
        if not chat:
            chat = DirectMessage.objects.create(sender_user=sender, receiver_user=receiver)

        message_text = request.data.get('text')
        if not message_text:
            return Response({'message': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        message = DirectMessage.objects.create(chat=chat, story=story, text=message_text)
        serializer = DirectMessageSerializer(message)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMessageToOpenStoryAPIView(APIView):
    """
    API view to send a direct message to the owner of an open story.

    Permissions:
    - IsAuthenticated: Only authenticated users can send messages.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        """
        Sends a direct message to the owner of a specific story.

        Args:
            story_id (int): The ID of the story whose owner will receive the message.
            request (Request): The request object containing message data.

        Returns:
            Response:
                - 201 Created: If the message was sent successfully, with serialized data.
                - 400 Bad Request: If the message data is invalid or missing.
                - 404 Not Found: If the story does not exist.
        """
        story = get_object_or_404(Story, id=story_id)
        sender = request.user
        receiver = story.user

        chat = DirectMessage.objects.filter(sender_user=sender, receiver_user=receiver)
        if not chat:
            chat = DirectMessage.objects.create(sender_user=sender, receiver_user=receiver)

        message_text = request.data.get('text')
        if not message_text:
            return Response({'message': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        message = DirectMessage.objects.create(chat=chat, story=story, text=message_text)
        serializer = DirectMessageSerializer(message)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from apis.permission_control import IsAuthenticated, AllowAny, TokenAuthentication
from posts.models import Story
from direct_messages.models import DirectMessage
from direct_messages.serializers import DirectMessageSerializer
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.serializers import StorySerializer


# Story APIS
class StoryListAPIView(APIView):
    """
    API view to retrieve a list of all stories.
    
    Permissions:
    - AllowAny: Any user, authenticated or not, can access this endpoint.
    """
    permission_classes = [AllowAny]

    def get(self):
        """
        Retrieve all stories, ordered by creation date in descending order.
        
        Returns:
            - 200 OK: List of stories serialized.
            - 400 Bad Request: If no stories exist.
        """
        story = Story.objects.all().order_by('-created_at')
        if story.exists():
            serializer = StorySerializer(story, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There is not such story'}, status=status.HTTP_400_BAD_REQUEST)


class StoryDetailAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific story.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this endpoint.
    
    Methods:
    - GET: Retrieves the details of a specific story.
    - DELETE: Deletes a specific story.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, story_id):
        """
        Retrieve the details of a specific story.

        Args:
            story_id (int): ID of the story to retrieve.

        Returns:
            - 200 OK: Serialized story data.
            - 404 Not Found: If the story does not exist.
        """
        post = get_object_or_404(Story, id=story_id)
        serializer = StorySerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, story_id):
        """
        Delete a specific story.
        
        Args:
            story_id (int): ID of the story to delete.

        Returns:
            - 204 No Content: If the story was deleted successfully.
        """
        story = get_object_or_404(Story, id=story_id)
        story.delete()
        return Response({'message': 'Story deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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
        Create a new story.

        Args:
            request (Request): The data for the new story.

        Returns:
            - 201 Created: If the story was created successfully.
            - 400 Bad Request: If the provided data is invalid.
        """
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryLikeAPIView(APIView):
    """
    API view to like or unlike a story and retrieve a list of likes for a story.
    
    Permissions:
    - IsAuthenticated: Only authenticated users can like or retrieve likes for a story.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        """
        Like or unlike a story.

        Args:
            story_id (int): ID of the story to like or unlike.

        Returns:
            - 200 OK: If the like is added or removed successfully.
            - 400 Bad Request: If the story cannot be found.
        """
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        like_instance = Like.objects.filter(user=user, story=story).first()
        if like_instance:
            like_instance.delete()
            story.like_count = max(0, story.like_count - 1)
            story.save()
            return Response({'detail': 'Like removed'}, status=status.HTTP_200_OK)

        Like.objects.create(user=user, story=story)
        story.like_count += 1
        story.save()
        return Response({'detail': 'Story liked'}, status=status.HTTP_200_OK)

    def get(self, request, story_id):
        """
        Retrieve a list of likes for a specific story.

        Args:
            story_id (int): ID of the story to get likes for.

        Returns:
            - 200 OK: List of likes serialized.
            - 403 Forbidden: If the user is not authorized to view likes for the story.
        """
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        if user == story.user or Like.objects.filter(user=user, story=story).exists():
            likes = Like.objects.filter(story=story)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'You are not authorized to view likes for this story.'}, status=status.HTTP_403_FORBIDDEN)


class SendMessageToStoryAPIView(APIView):
    """
    API view to send a message to a story's owner via direct message.
    
    Permissions:
    - IsAuthenticated: Only authenticated users can send messages.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        """
        Send a message to the owner of a specific story.
        
        Args:
            story_id (int): ID of the story to send a message to.
            request (Request): The message data to send.

        Returns:
            - 201 Created: If the message was sent successfully.
            - 400 Bad Request: If the message data is invalid.
        """
    def post(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        sender = request.user
        reciever = story.user

        chat = DirectMessage.objects.filter(sender_user=sender, reciever_user=reciever)
        if not chat:
            chat = DirectMessage.objects.create(sender_user=sender, reciever_user=reciever)

        message_text = request.data.get('text')
        if not message_text:
            return Response({'error': 'message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        message = DirectMessage.objects.create(chat=chat, story=story, text=message_text)
        serializer = DirectMessageSerializer(message)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







    
       
       

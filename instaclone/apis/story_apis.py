from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from apis.permission_control import HeHasPermission, BasePermission, IsAuthenticated, AllowAny, TokenAuthentication
from posts.models import Story
from comments.models import Comment
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.serializers import PostSerializer, StorySerializer
from comments.serializers import CommentSerializer


#Story APIS
class StoryListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self):
        story = Story.objects.all().order_by('-created_at')
        if story.exists():
            serializer = StorySerializer(story, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message':'There is not such story'}, status=status.HTTP_400_BAD_REQUEST)


class StoryDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, story_id):
        post = get_object_or_404(Story, id=story_id)
        serializer = StorySerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self, story_id):
        story = get_object_or_404(Story, id=story_id)
        story.delete()
        return Response({'message': 'Story deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class StoryCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryLikeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, story_id):
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
        story = get_object_or_404(Story, id=story_id)
        user = request.user
        if user == story.user or Like.objects.filter(user=user, story=story).exists():
            likes = Like.objects.filter(story=story)
            serializer = LikeSerializer(likes, many=True)
            return Response (serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'You are not authorized to view likes for this story.'}, status=status.HTTP_403_FORBIDDEN)





    
       
       

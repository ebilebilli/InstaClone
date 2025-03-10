from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny

from posts.models import Post, Story, User
from comments.models import Comment
from likes.models import Like
from posts.serializers import PostSerializer, StorySerializer
from comments.serializers import CommentSerializer


class HeHasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff

#Post APIS
class PostListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self):
        post = Post.objects.all().order_by('-created_at')
        if post.exists():
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message':'There are not any posts yet'}, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        caption_data = {'caption': request.data.get('caption', post.caption)}
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class PostCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        like_instance = Like.objects.filter(user=user, post=post).first()

        if like_instance:
            like_instance.delete()
            post.like_count = max(0, post.like - 1)
            post.save()
            return Response({'detail': 'Like removed'}, status=status.HTTP_200_OK)

        Like.objects.create(user=user, post=post)
        post.like_count += 1
        post.save()
        return Response({'detail': "post liked"}, status=status.HTTP_200_OK)


class PostCommentManagementSection(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, post_id):
        serializer = CommentSerializer(request.data)
        post = get_object_or_404(Post, id=post_id)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        comment = Comment.objects.filter(post_id=post_id)
        if comment.exists():
            serializer = CommentSerializer(comment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response ({'Message': 'There are not any comments'}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


    
       
       

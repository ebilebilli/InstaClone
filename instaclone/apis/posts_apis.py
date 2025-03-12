from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from apis.permission_control import HeHasPermission, IsAuthenticated, AllowAny, TokenAuthentication
from posts.models import Post
from comments.models import Comment
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer


# Post APIS
class PostListAPIView(APIView):
    """
    API view to list all posts.

    Permission:
        - AllowAny: This view is accessible by any user.
    
    Methods:
        GET:
            Retrieves all posts ordered by creation date.
    """
    
    permission_classes = [AllowAny]
    
    def get(self):
        post = Post.objects.all().order_by('-created_at')
        if post.exists():
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There are not any posts yet'}, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    """
    API view to retrieve, update, and delete a specific post.

    Permission:
        - IsAuthenticated: Only authenticated users can access this view.
    
    Methods:
        GET:
            Retrieves the details of a specific post.
        
        PATCH:
            Partially updates the caption of a specific post.
        
        DELETE:
            Deletes a specific post.
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    """
    API view to create a new post.

    Permission:
        - IsAuthenticated: Only authenticated users can create posts.
    
    Methods:
        POST:
            Creates a new post with the provided data.
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeAPIView(APIView):
    """
    API view to like or unlike a post.

    Permission:
        - IsAuthenticated: Only authenticated users can like/unlike posts.
    
    Methods:
        POST:
            Likes or unlikes a post.
        
        GET:
            Retrieves a list of likes for a specific post.
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        like_instance = Like.objects.filter(user=user, post=post).first()

        if like_instance:
            like_instance.delete()
            post.like_count = max(0, post.like_count - 1)
            post.save()
            return Response({'detail': 'Like removed'}, status=status.HTTP_200_OK)

        Like.objects.create(user=user, post=post)
        post.like_count += 1
        post.save()
        return Response({'detail': 'Post liked'}, status=status.HTTP_200_OK)
    
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        likes = Like.objects.filter(post=post)
        if likes.exists():
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There are not any likes yet'}, status=status.HTTP_404_NOT_FOUND)


class PostCommentManagementSection(APIView):
    """
    API view to manage comments on posts (create, retrieve, update, delete).

    Permission:
        - IsAuthenticated: Only authenticated users can create or update comments.
        - HeHasPermission: Custom permission to manage specific comments.
    
    Methods:
        POST:
            Creates a new comment for a post.
        
        GET:
            Retrieves all comments for a specific post.
        
        PATCH:
            Updates a specific comment.
        
        DELETE:
            Deletes a specific comment.
    """
    
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
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        if comments.exists():
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There are not any comments'}, status=status.HTTP_404_NOT_FOUND)
    
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


class CommentLikeAPIView(APIView):
    """
    API view to like or unlike a comment.

    Permission:
        - IsAuthenticated: Only authenticated users can like/unlike comments.
    
    Methods:
        POST:
            Likes or unlikes a comment.
        
        GET:
            Retrieves a list of likes for a specific comment.
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user
        like_instance = Like.objects.filter(user=user, comment=comment).first()

        if like_instance:
            like_instance.delete()
            comment.like_count = max(0, comment.like_count - 1)
            comment.save()
            return Response({'detail': 'Like removed'}, status=status.HTTP_200_OK)

        Like.objects.create(user=user, comment=comment)
        comment.like_count += 1
        comment.save()
        return Response({'detail': 'Comment liked'}, status=status.HTTP_200_OK)
    
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        likes = Like.objects.filter(comment=comment)
        if likes.exists():
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There are not any likes yet'}, status=status.HTTP_404_NOT_FOUND)

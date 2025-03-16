from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from apis.permission_control import HeHasPermission, IsAuthenticated, AllowAny, TokenAuthentication, IsOwner
from posts.models import Post
from profiles.models import Profile
from comments.models import Comment
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer


# Post APIs
class OpenPostListAPIView(APIView):
    """
    API view to retrieve a list of all posts from profiles with open visibility.

    Permissions:
        - AllowAny: Accessible to any user, authenticated or not.

    Methods:
        GET:
            Retrieves all posts from profiles with 'OPEN_PROFILE' status, ordered by creation date (newest first).
            Returns a serialized list of posts or an error if none exist.
    """
    permission_classes = [AllowAny]

    def get(self, request):  
        """
        Handles GET requests to retrieve posts from open profiles.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response:
                - 200 OK: A serialized list of posts if any exist.
                - 400 Bad Request: If no posts are found.
        """
        post = Post.objects.filter(profile__profile_status=Profile.OPEN_PROFILE).order_by('-created_at')
        if post.exists():
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no posts available yet.'}, status=status.HTTP_400_BAD_REQUEST)


class PrivatePostListAPIView(APIView):
    """
    API view to retrieve a list of posts visible to authenticated users with specific permissions.

    Permissions:
        - IsAuthenticated: Requires user authentication.
        - HeHasPermission: Requires additional custom permission.

    Methods:
        GET:
            Retrieves all posts from profiles with 'OPEN_PROFILE' status, ordered by creation date (newest first).
            Returns a serialized list of posts or an error if none exist.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request):  
        """
        Handles GET requests to retrieve posts from open profiles for authorized users.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response:
                - 200 OK: A serialized list of posts if any exist.
                - 400 Bad Request: If no posts are found.
        """
        post = Post.objects.filter(profile__profile_status=Profile.OPEN_PROFILE).order_by('-created_at')
        if post.exists():
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no posts available yet.'}, status=status.HTTP_400_BAD_REQUEST)


class PrivatePostDetailAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific post for authorized users.

    Permissions:
        - IsAuthenticated: Requires user authentication.
        - HeHasPermission: Requires additional custom permission.

    Methods:
        GET:
            Retrieves details of a specific post by its ID.
        PATCH:
            Partially updates the caption of a specific post, restricted to the post owner.
        DELETE:
            Deletes a specific post, restricted to the post owner.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, post_id): 
        """
        Handles GET requests to retrieve a specific post's details.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to retrieve.

        Returns:
            Response:
                - 200 OK: Serialized post data.
                - 404 Not Found: If the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, post_id, *args, **kwargs):
        """
        Handles PATCH requests to partially update a specific post's caption.

        Args:
            request (Request): The HTTP request object containing update data.
            post_id (int): The ID of the post to update.

        Returns:
            Response:
                - 200 OK: Updated serialized post data if successful.
                - 400 Bad Request: If the user is unauthorized or data is invalid.
                - 404 Not Found: If the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        caption_data = {'caption': request.data.get('caption', post.caption)}
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        """
        Handles DELETE requests to remove a specific post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to delete.

        Returns:
            Response:
                - 204 No Content: If the post is deleted successfully.
                - 400 Bad Request: If the user is unauthorized.
                - 404 Not Found: If the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response({'message': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class OpenPostDetailAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific post for authenticated users.

    Permissions:
        - IsAuthenticated: Requires user authentication.

    Methods:
        GET:
            Retrieves details of a specific post by its ID.
        PATCH:
            Partially updates the caption of a specific post, restricted to the post owner.
        DELETE:
            Deletes a specific post, restricted to the post owner.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):  
        """
        Handles GET requests to retrieve a specific post's details.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to retrieve.

        Returns:
            Response:
                - 200 OK: Serialized post data.
                - 404 Not Found: If the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, post_id, *args, **kwargs):
        """
        Handles PATCH requests to partially update a specific post's caption.

        Args:
            request (Request): The HTTP request object containing update data.
            post_id (int): The ID of the post to update.

        Returns:
            Response:
                - 200 OK: Updated serialized post data if successful.
                - 400 Bad Request: If the user is unauthorized or data is invalid.
                - 404 Not Found: If the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        caption_data = {'caption': request.data.get('caption', post.caption)}
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        """
        Handles DELETE requests to remove a specific post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to delete.

        Returns:
            Response:
                - 204 No Content: If the post is deleted successfully.
                - 400 Bad Request: If the user is unauthorized.
                - 404 Not Found: If the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response({'message': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class PostCreateAPIView(APIView):
    """
    API view to create a new post for authenticated users.

    Permissions:
        - IsAuthenticated: Requires user authentication.

    Methods:
        POST:
            Creates a new post with the provided data.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to create a new post.

        Args:
            request (Request): The HTTP request object containing post data.

        Returns:
            Response:
                - 201 Created: Serialized post data if creation is successful.
                - 400 Bad Request: If the provided data is invalid.
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenPostLikeAPIView(APIView):
    """
    API view to like/unlike a post or retrieve its likes for authenticated users.

    Permissions:
        - IsAuthenticated: Requires user authentication.

    Methods:
        POST:
            Toggles like status for a specific post.
        GET:
            Retrieves a list of likes for a specific post.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Handles POST requests to like or unlike a post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to like/unlike.

        Returns:
            Response:
                - 200 OK: Confirmation message if like is added or removed.
                - 404 Not Found: If the post does not exist.
        """
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
        """
        Handles GET requests to retrieve likes for a specific post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to retrieve likes for.

        Returns:
            Response:
                - 200 OK: A serialized list of likes if any exist.
                - 404 Not Found: If no likes are found or the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        likes = Like.objects.filter(post=post)
        if likes.exists():
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no likes yet.'}, status=status.HTTP_404_NOT_FOUND)


class PrivatePostLikeAPIView(APIView):
    """
    API view to like/unlike a post or retrieve its likes for authorized users.

    Permissions:
        - IsAuthenticated: Requires user authentication.
        - HeHasPermission: Requires additional custom permission.

    Methods:
        POST:
            Toggles like status for a specific post.
        GET:
            Retrieves a list of likes for a specific post.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, post_id):
        """
        Handles POST requests to like or unlike a post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to like/unlike.

        Returns:
            Response:
                - 200 OK: Confirmation message if like is added or removed.
                - 404 Not Found: If the post does not exist.
        """
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
        """
        Handles GET requests to retrieve likes for a specific post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to retrieve likes for.

        Returns:
            Response:
                - 200 OK: A serialized list of likes if any exist.
                - 404 Not Found: If no likes are found or the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        likes = Like.objects.filter(post=post)
        if likes.exists():
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no likes yet.'}, status=status.HTTP_404_NOT_FOUND)


class PostCommentManagementSection(APIView):
    """
    API view to manage comments on posts (create, retrieve, update, delete).

    Permissions:
        - IsAuthenticated: Requires user authentication.
        - IsOwner: Restricts updates and deletions to the comment owner.

    Methods:
        POST:
            Creates a new comment for a specific post.
        GET:
            Retrieves all comments for a specific post.
        PATCH:
            Updates a specific comment, restricted to the owner.
        DELETE:
            Deletes a specific comment, restricted to the owner.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, post_id):
        """
        Handles POST requests to create a new comment on a post.

        Args:
            request (Request): The HTTP request object containing comment data.
            post_id (int): The ID of the post to comment on.

        Returns:
            Response:
                - 201 Created: Serialized comment data if creation is successful.
                - 400 Bad Request: If the data is invalid.
                - 404 Not Found: If the post does not exist.
        """
        serializer = CommentSerializer(data=request.data)  
        post = get_object_or_404(Post, id=post_id)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        """
        Handles GET requests to retrieve all comments for a post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to retrieve comments for.

        Returns:
            Response:
                - 200 OK: A serialized list of comments if any exist.
                - 404 Not Found: If no comments are found or the post does not exist.
        """
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        if comments.exists():
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no comments yet.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, comment_id):
        """
        Handles PATCH requests to update a specific comment.

        Args:
            request (Request): The HTTP request object containing update data.
            comment_id (int): The ID of the comment to update.

        Returns:
            Response:
                - 200 OK: Updated serialized comment data if successful.
                - 400 Bad Request: If the user is unauthorized or data is invalid.
                - 404 Not Found: If the comment does not exist.
        """
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """
        Handles DELETE requests to remove a specific comment.

        Args:
            request (Request): The HTTP request object.
            comment_id (int): The ID of the comment to delete.

        Returns:
            Response:
                - 204 No Content: If the comment is deleted successfully.
                - 400 Bad Request: If the user is unauthorized.
                - 404 Not Found: If the comment does not exist.
        """
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CommentLikeAPIView(APIView):
    """
    API view to like/unlike a comment or retrieve its likes for authenticated users.

    Permissions:
        - IsAuthenticated: Requires user authentication.

    Methods:
        POST:
            Toggles like status for a specific comment.
        GET:
            Retrieves a list of likes for a specific comment.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request, comment_id):
        """
        Handles POST requests to like or unlike a comment.

        Args:
            request (Request): The HTTP request object.
            comment_id (int): The ID of the comment to like/unlike.

        Returns:
            Response:
                - 200 OK: Confirmation message if like is added or removed.
                - 404 Not Found: If the comment does not exist.
        """
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
        """
        Handles GET requests to retrieve likes for a specific comment.

        Args:
            request (Request): The HTTP request object.
            comment_id (int): The ID of the comment to retrieve likes for.

        Returns:
            Response:
                - 200 OK: A serialized list of likes if any exist.
                - 404 Not Found: If no likes are found or the comment does not exist.
        """
        comment = get_object_or_404(Comment, id=comment_id)
        likes = Like.objects.filter(comment=comment)
        if likes.exists():
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There are no likes yet.'}, status=status.HTTP_404_NOT_FOUND)
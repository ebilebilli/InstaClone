from django.urls import path
from .posts_apis import *
from .story_apis import *


app_name = 'apis'

urlpatterns = [path('posts/', PostListAPIView.as_view(), name='posts'),
               path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
               path('post_detail/<int:post_id>/', PostDetailAPIView.as_view(), name='post_detail'),
               path('post/<int:post_id>/like_post/', PostLikeAPIView.as_view(), name='like_post'),
               path('post/<int:post_id>/comments/', PostCommentManagementSection.as_view(), name='post_comments'),
               path('post/<int:comment_id>/', PostCommentManagementSection.as_view(), name='comment_update'),
               path('post/<int:comment_id>/like_comment', CommentLikeAPIView.as_view(), name='comment_like'),
               path('stories/', StoryListAPIView.as_view(), name='stories'),
               path('story_create/', StoryCreateAPIView.as_view(), name='story_create'),
               path('story_detail/<int:story_id>/', StoryDetailAPIView.as_view(), name='story_detail'),
               path('story/<int:story_id>/like_story', StoryLikeAPIView.as_view(), name='like_story')


]


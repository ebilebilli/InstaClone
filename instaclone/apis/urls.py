from django.urls import path
from .post_apis import *
from .story_apis import *
from .profile_apis import *


app_name = 'apis'

urlpatterns = [path('open_posts/', OpenPostListAPIView.as_view(), name='posts'),
               path('private_posts/', PrivatePostListAPIView.as_view(), name='posts'),
               path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
               path('private_post_detail/<int:post_id>/', PrivatePostDetailAPIView.as_view(), name='post_detail'),
               path('open_post_detail/<int:post_id>/', OpenPostDetailAPIView.as_view(), name='post_detail'),
               path('open_post/<int:post_id>/like_post/', OpenPostLikeAPIView.as_view(), name='like_post'),
               path('private_post/<int:post_id>/like_post/', PrivatePostLikeAPIView.as_view(), name='like_post'),
               path('post/<int:post_id>/comments/', PostCommentManagementSection.as_view(), name='post_comments'),
               path('post/<int:comment_id>/', PostCommentManagementSection.as_view(), name='comment_update'),
               path('post/<int:comment_id>/like_comment', CommentLikeAPIView.as_view(), name='comment_like'),
               path('stories/', OpenStoryListAPIView.as_view(), name='open-stories'),
               path('story_create/', StoryCreateAPIView.as_view(), name='story_create'),
               path('open_story_detail/<int:story_id>/', OpenStoryDetailAPIView.as_view(), name='open_story_detail'),
               path('private_story_detail/<int:story_id>/', PrivateStoryDetailAPIView.as_view(), name='private_story_detail'),
               path('private_story/<int:story_id>/like_story', PrivateStoryLikeAPIView.as_view(), name='like_private_story'),
               path('open_story/<int:story_id>/like_story', OpenStoryLikeAPIView.as_view(), name='like_open_story'),
               path('open_story/<int:story_id>/send_message_to_story', SendMessageToOpenStoryAPIView.as_view(), name='send_message_to_story'),
               path('private_story/<int:story_id>/send_message_to_story', SendMessageToPrivateStoryAPIView.as_view(), name='send_message_to_story'),
               path('profiles/search', ProfileSearchAPIView.as_view(), name='search_profile'),
               path('profile_detail/<int:profile_id>/', ProfileDetailAPIView.as_view(), name='profile_detail'),
               path('profile_followers/<int:profile_id>/', ProfileFollowerListAPIView.as_view(), name='profile_followers'),
               path('profile_followings/<int:profile_id>/', ProfileFollowingListAPIView.as_view(), name='profile_followings'),

]


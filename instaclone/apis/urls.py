from django.urls import path
from .posts_apis import *


app_name = 'apis'

urlpatterns = [path('posts/', PostListAPIView.as_view(), name='posts'),
               path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
               path('post_detail/<int:post_id>/', PostDetailAPIView.as_view(), name='post_detail'),
               path('post/<int:post_id>/like_post/', PostLikeAPIView.as_view(), name='like_post'),
               path('post/<int:post_id>/comments/', PostCommentManagementSection.as_view(), name='post_comments')
]
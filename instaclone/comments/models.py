from django.db import models
from posts.models import Post, User, Story


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    story =  models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')

    text = models.CharField(max_length=2200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.text[:20]}'



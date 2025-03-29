from django.db import models
from posts.models import Post, Story
from comments.models import Comment
from profiles.models import CustomerUser

# Create your models here.

class Like(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'post'), ('user', 'comment'), ('user', 'story')]
    
    def __str__(self):
        if self.post:
            content = 'post'
        elif self.story :
            content= 'story'
        elif self.comment:
            content = 'comment'
        return f'{content} liked by {self.user.username}'
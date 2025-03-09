from django.db import models
from posts.models import User, Post, Story


class DirectMessage(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_messages', null=True, blank=True)
    story =  models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_messages', null=True, blank=True)

    text = models.CharField(max_length=2200)
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    video = models.FileField(upload_to='message_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender_user.username} to {self.receiver_user.username}'
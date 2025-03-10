from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    caption = models.CharField(max_length=2200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')

    caption = models.CharField(max_length=2200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def time_limit(self):
        one_day = now() - timedelta(hours=24)
        return one_day
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'

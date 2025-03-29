from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from profiles.models import CustomerUser


class Post(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='posts')

    caption = models.CharField(max_length=2200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'


class Story(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='stories')

    caption = models.CharField(max_length=2200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)

    @classmethod
    def visible_stories(cls):
        return cls.objects.filter(created_at__gte=now() - timedelta(hours=24))
    
    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'

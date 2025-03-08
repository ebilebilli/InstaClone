from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    caption = models.CharField(max_length=2200, null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'
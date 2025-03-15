from django.db import models
from posts.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    followers = models.ManyToManyField(User, related_name='followings', symmetrical=False, blank=True)

    OPEN_PROFILE = 'Open Profile'
    PRIVATE_PROFILE = 'Private Profile'

    STATUS_LIST = [
        (OPEN_PROFILE, 'Open Profile'),
        (PRIVATE_PROFILE, 'Private Profile')
    ]

    profile_status = models.CharField(max_length=25, choices=STATUS_LIST, default=OPEN_PROFILE)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'
    

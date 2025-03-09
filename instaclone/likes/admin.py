from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment', 'story', 'created_at')
    list_filter = ('created_at', 'post', 'story', 'comment')
    search_fields = ('user__username', 'post__title', 'story_caption', 'comment__text')
    ordering = ('-created_at',)

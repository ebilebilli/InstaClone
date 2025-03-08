from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'image', 'video') 
    search_fields = ('user__username', 'caption')  
    list_filter = ('created_at',)  
admin.site.register(Post, PostAdmin)

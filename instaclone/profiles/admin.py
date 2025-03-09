from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'bio', 'website_link', 'created_at') 
    search_fields = ('user__username', 'bio') 
    list_filter = ('created_at',) 
    ordering = ('-created_at',) 
admin.site.register(Profile, ProfileAdmin)
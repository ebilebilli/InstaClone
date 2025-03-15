from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_status', 'profile_picture', 'bio', 'website_link', 'created_at')  
    search_fields = ('user__username', 'bio', 'website_link')  
    list_filter = ('profile_status', 'created_at')  
    ordering = ('-created_at',)  
    readonly_fields = ('created_at',)  

admin.site.register(Profile, ProfileAdmin)

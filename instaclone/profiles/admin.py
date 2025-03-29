from django.contrib import admin
from .models import CustomerUser, Profile


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')
    

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_status', 'bio', 'website_link', 'created_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('profile_status', 'created_at')

admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(Profile, ProfileAdmin)

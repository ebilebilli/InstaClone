from django.contrib import admin
from .models import DirectMessage

@admin.register(DirectMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_user', 'receiver_user', 'created_at', 'text_preview')
    search_fields = ('sender_user__username', 'receiver_user__username', 'text')
    list_filter = ('created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Text Preview'

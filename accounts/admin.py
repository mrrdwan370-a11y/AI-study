from django.contrib import admin
from django.utils.html import format_html
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( "avatar_preview", "user", "phone", "created_at", )
    search_fields = ( "user__username", "user__email","phone",)
    list_filter = ( "created_at", )
    readonly_fields = ( "avatar_preview", )
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html( '<img src="{}" width="55" height="55" ' 'style="border-radius:50%; object-fit:cover;" />',
                obj.avatar.url )
        return "No Avatar"
    avatar_preview.short_description = "Avatar"
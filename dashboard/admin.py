from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "user",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "action",
        "description",
    )
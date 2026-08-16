from django.contrib import admin
from .models import Note, Category, Tag


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "is_favorite",
        "created_at",
    )
    list_filter = ("category", "is_favorite", "created_at")
    search_fields = ("title", "content")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name",)
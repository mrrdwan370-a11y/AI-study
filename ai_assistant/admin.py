from django.contrib import admin

# from .models import  AIMessage


# @admin.register(AIConversation)
# class AIConversationAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "user",
#         "created_at",
#         "updated_at",
#     )

#     search_fields = (
#         "title",
#         "user__username",
#     )


# @admin.register(AIMessage)
# class AIMessageAdmin(admin.ModelAdmin):
#     list_display = (
#         "conversation",
#         "role",
#         "created_at",
#     )

#     list_filter = ("role",)

#     search_fields = ("content",)
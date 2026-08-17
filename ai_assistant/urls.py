from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.ai_chat,
        name="ai_chat"
    ),
    path(
    "delete/<int:session_id>/",
    views.delete_chat,
    name="delete_chat"
),

]
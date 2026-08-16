from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.task_list,
        name="tasks_list"
    ),

    path(
        "create/",
        views.task_create,
        name="task_create"
    ),

    path(
        "<int:pk>/edit/",
        views.task_update,
        name="task_update"
    ),

    path(
        "<int:pk>/delete/",
        views.task_delete,
        name="task_delete"
    ),

    path(
        "<int:pk>/complete/",
        views.task_complete,
        name="task_complete"
    ),

    # 🤖 Solve Task With AI
    path(
        "<int:pk>/solve-ai/",
        views.solve_task_with_ai,
        name="solve_task_with_ai"
    ),
]
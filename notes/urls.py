from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.notes_list,
        name="notes_list"
    ),

    path(
        "create/",
        views.note_create,
        name="note_create"
    ),

    path(
        "<int:pk>/",
        views.note_detail,
        name="note_detail"
    ),
path(
    "live-search/",
    views.notes_live_search,
    name="notes_live_search"
),
    path(
        "<int:pk>/edit/",
        views.note_update,
        name="note_update"
    ),

    path(
        "<int:pk>/delete/",
        views.note_delete,
        name="note_delete"
    ),

    path(
        "<int:pk>/favorite/",
        views.note_toggle_favorite,
        name="note_toggle_favorite"
    ),

    path(
        "categories/create/",
        views.category_create,
        name="category_create"
    ),

    path(
        "tags/create/",
        views.tag_create,
        name="tag_create"

    ),




    

    path(
        "summarize-note/<int:pk>/",
        views.summarize_note,
        name="summarize_note"
    ),


]
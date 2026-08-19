from django.urls import path
from . import views


urlpatterns = [
    path(  "",  views.resources_list,  name="resources_list"  ),
    path(  "create/", views.resource_create, name="resource_create" ),
    path(  "<int:pk>/", views.resource_detail,  name="resource_detail" ),
    path(  "<int:pk>/edit/",  views.resource_update,  name="resource_update" ),
    path( "<int:pk>/delete/",  views.resource_delete,  name="resource_delete" ),
]
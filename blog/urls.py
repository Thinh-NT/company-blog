from django.urls import path
from .views import index, post, blog, search, update_post, delete_post, create_post

urlpatterns = [
    path("", index, name="index"),
    path("blog/", blog, name="blog"),
    path("post/<id>/", post, name="detail-post"),
    path("post/<id>/update", update_post, name="update-post"),
    path("post/<id>/delete", delete_post, name="delete-post"),
    path("search/", search, name="search"),
    path("create/", create_post, name="create"),
]

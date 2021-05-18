from django.urls import path
from .views import index, post, blog, search

urlpatterns = [
    path("", index, name="index"),
    path("blog/", blog, name="blog"),
    path("post/<id>/", post, name="detail-post"),
    path("search", search, name="search"),
]

from django.urls import path
from .views import index, post, blog

urlpatterns = [
    path("", index, name="index"),
    path("blog/", blog, name="blog"),
    path("post/<id>/", post, name="detail-post"),
]

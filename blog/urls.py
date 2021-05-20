from django.urls import path
from .views import (index, post, blog, search, create_post, profile,
                    PostDeleteView, PostUpdateView,
                    category_posts_view)

urlpatterns = [
    path("", index, name="index"),
    path("profile/", profile, name="profile"),
    path("blog/", blog, name="blog"),
    path("post/<id>/", post, name="detail-post"),
    path("search/", search, name="search"),
    path("create/", create_post, name="create"),
    path("category/<category>", category_posts_view, name="category-posts"),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]

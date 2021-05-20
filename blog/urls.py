from django.urls import path
from .views import (index, post, blog, search,
                    update_post, delete_post, create_post, profile,
                    PostDeleteView, PostUpdateView,
                    post_delete, post_update)

urlpatterns = [
    path("", index, name="index"),
    path("profile/", profile, name="profile"),
    path("blog/", blog, name="blog"),
    path("post/<id>/", post, name="detail-post"),
    path("post/<id>/update", update_post, name="update-post"),
    path("post/<id>/delete", delete_post, name="delete-post"),
    path("search/", search, name="search"),
    path("create/", create_post, name="create"),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('post/<id>/update/', post_update, name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
]

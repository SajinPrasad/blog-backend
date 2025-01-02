from django.urls import path

from .views import (
    post_create_view,
    post_list_view,
    post_delete_view,
    post_retrieve_view,
    post_edit_view,
    list_my_posts,
)

urlpatterns = [
    path("api/create-post/", post_create_view, name="create-post"),
    path("api/posts/", post_list_view, name="post-list"),
    path("api/posts/<int:id>/", post_retrieve_view, name="post-retrieve"),
    path("api/delete/<int:id>/", post_delete_view, name="post-delete"),
    path("api/edit/<int:id>/", post_edit_view, name="post-delete"),
    path("api/myposts/", list_my_posts, name="my-posts"),
]

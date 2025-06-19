from django.urls import path

from .views import BlogPostDetailView, BlogPostListCreateView, CommentCreateView

urlpatterns = [
    path("posts/", BlogPostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", BlogPostDetailView.as_view(), name="post-detail"),
    path(
        "posts/<int:pk>/comments/",
        CommentCreateView.as_view(),
        name="post-comment-create",
    ),
]

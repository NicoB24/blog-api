from typing import Any, Optional

from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BlogPost
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    CommentSerializer,
)


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BlogPost to handle CRUD operations and adding comments.
    """

    queryset = BlogPost.objects.annotate(comment_count=Count("comments"))

    def get_serializer_class(self):
        """
        Return different serializer classes depending on the action.
        - list: BlogPostListSerializer (with comment_count)
        - retrieve: BlogPostDetailSerializer (with comments)
        - others (create, update): BlogPostDetailSerializer
        """
        if self.action == "list":
            return BlogPostListSerializer
        elif self.action == "retrieve":
            return BlogPostDetailSerializer
        return BlogPostDetailSerializer

    @action(detail=True, methods=["post"])
    def comments(self, request: Any, pk: Optional[str] = None) -> Response:
        """
        Custom action to create a comment for a specific blog post.
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

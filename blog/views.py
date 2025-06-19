from rest_framework import generics

from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostSerializer, CommentSerializer


class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BlogPostListSerializer
        return BlogPostSerializer


class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        post = BlogPost.objects.get(pk=post_id)
        serializer.save(post=post)

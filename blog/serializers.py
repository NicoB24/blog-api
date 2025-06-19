from typing import Any

from rest_framework import serializers

from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model without created_at field.
    """

    class Meta:
        model = Comment
        fields = ["id", "content"]  # Only id and content


class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing BlogPosts with comment_count only.
    """

    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "comment_count"]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single BlogPost with comments list.
    """

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "comments"]

    def create(self, validated_data: dict[str, Any]) -> BlogPost:
        """
        Create and return a new BlogPost instance.
        """
        return super().create(validated_data)

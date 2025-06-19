from rest_framework import serializers

from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content"]
        read_only_fields = ["id", "created_at"]


class BlogPostListSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "comment_count"]


class BlogPostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "comments"]

    def get_comments(self, obj):
        comments = obj.comments.order_by("created_at")
        return CommentSerializer(comments, many=True).data

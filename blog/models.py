from django.db import models


class BlogPost(models.Model):
    """
    Model representing a blog post.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        String representation of the BlogPost instance.
        """
        return self.title


class Comment(models.Model):
    """
    Model representing a comment associated with a blog post.
    """

    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        String representation of the Comment instance.
        """
        return f"Comment on {self.post.title}"

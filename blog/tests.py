import pytest
from rest_framework.test import APIClient

from blog.models import BlogPost, Comment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_post():
    return BlogPost.objects.create(title="Test Post", content="Content here")


@pytest.fixture
def sample_comments(sample_post):
    comments = [
        Comment.objects.create(post=sample_post, content="Comment 1"),
        Comment.objects.create(post=sample_post, content="Comment 2"),
    ]
    return comments


@pytest.mark.django_db
def test_list_posts_includes_comment_count(api_client, sample_post, sample_comments):
    # Add comments for the post are created via fixture
    url = "/api/posts/"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    post_data = data[0]
    assert "id" in post_data
    assert post_data["title"] == sample_post.title
    assert post_data["content"] == sample_post.content
    assert "comment_count" in post_data
    assert post_data["comment_count"] == len(sample_comments)
    assert (
        "comments" not in post_data
    )  # comments list should NOT be present in list endpoint


@pytest.mark.django_db
def test_retrieve_post_includes_comments_not_comment_count(
    api_client, sample_post, sample_comments
):
    url = f"/api/posts/{sample_post.id}/"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["title"] == sample_post.title
    assert data["content"] == sample_post.content
    assert "comments" in data
    assert isinstance(data["comments"], list)
    assert len(data["comments"]) == len(sample_comments)
    assert (
        "comment_count" not in data
    )  # comment_count should NOT be present in retrieve

    for comment_data, comment in zip(data["comments"], sample_comments):
        assert comment_data["id"] == comment.id
        assert comment_data["content"] == comment.content


@pytest.mark.django_db
def test_create_post(api_client):
    url = "/api/posts/"
    payload = {"title": "New Post", "content": "Some content"}

    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "id" in data


@pytest.mark.django_db
def test_create_post_validation_error(api_client):
    url = "/api/posts/"
    payload = {"content": "Missing title"}

    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 400
    assert "title" in response.json()


@pytest.mark.django_db
def test_create_comment(api_client, sample_post):
    url = f"/api/posts/{sample_post.id}/comments/"
    payload = {"content": "A new comment"}

    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == payload["content"]
    assert "id" in data

    # Confirm the comment is associated with the post
    comments = Comment.objects.filter(post=sample_post)
    assert comments.filter(content=payload["content"]).exists()


@pytest.mark.django_db
def test_comments_list_not_accessible_directly(api_client):
    # There is no endpoint /api/comments/ so it should 404
    response = api_client.get("/api/comments/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_list_post_does_not_return_unwanted_fields(api_client, sample_post):
    url = "/api/posts/"
    response = api_client.get(url)
    data = response.json()[0]

    # Ensure only the specified fields are returned
    allowed_fields = {"id", "title", "content", "comment_count"}
    assert set(data.keys()) == allowed_fields


@pytest.mark.django_db
def test_retrieve_post_does_not_return_unwanted_fields(api_client, sample_post):
    url = f"/api/posts/{sample_post.id}/"
    response = api_client.get(url)
    data = response.json()

    # Allowed fields in detail
    allowed_fields = {"id", "title", "content", "comments"}
    assert set(data.keys()) == allowed_fields

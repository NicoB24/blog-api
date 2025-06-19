# 📝 Blog API

**RESTful API for managing a simple blogging platform.**  
The core functionality of this platform includes managing blog posts and their associated comments.

---

## 📦 Tech Stack

- **Python** 3.12  
- **Django** 5.0.6  
- **Django REST Framework** 3.15.1  
- **PostgreSQL** 16  
- **Docker** & **Docker Compose**  
- Linters & formatters: `black`, `isort`, `flake8`, `mypy`  
- Tests: `pytest`

---

## 🚀 Getting Started

### 🔧 Requirements

- Docker  
- Docker Compose

---

### Setup

1. **Clone the repository**

```
git clone https://github.com/NicoB24/blog-api.git
cd blog-api
```


2. **Create a .env file**
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
```

3. **Build and run the project**

```
docker-compose up --build
```

The API will be available at:
👉 http://localhost:8000/api/posts/



## Endpoint calling examples using curl

### Get all posts
```
curl -X GET http://127.0.0.1:8000/api/posts/
```

### Create a new post
```
curl -X POST http://127.0.0.1:8000/api/posts/ \
-H "Content-Type: application/json" \
-d '{"title": "New Post", "content": "This is the content of the post."}'
```

### Get a single post
```
curl -X GET http://127.0.0.1:8000/api/posts/1/
```

### Add a comment to a post
```
curl -X POST http://127.0.0.1:8000/api/posts/1/comments/ \
-H "Content-Type: application/json" \
-d '{"content": "This is a new comment."}'
```

## 🧪 Run Tests
```
docker-compose exec web pytest
```

## 🧹 Code Quality
```
docker-compose exec web bash -c "
  black . &&
  isort . &&
  flake8 . &&
  mypy .
"
```

or you can run them individually
```
docker-compose exec web black .
docker-compose exec web isort .
docker-compose exec web flake8 .
docker-compose exec web mypy .
```

## Future Improvements
- Authentication and Permissions (JWT or OAuth2-based authentication, add per-user access control)
- API Pagination and Filtering
- Validation and Error Handling (Improve error responses add field-level validations)
- API documentation
- Logging & Monitoring
- Add production and testing settings

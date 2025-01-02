from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.title}"

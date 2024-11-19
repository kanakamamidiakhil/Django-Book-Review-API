from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    cover_image_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    genre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source='id', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'ISBN', 'created_at', 'genre', 'average_rating']
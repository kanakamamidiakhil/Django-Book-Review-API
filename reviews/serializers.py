from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    review_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Review
        fields = ['review_id', 'user', 'book', 'rating', 'content', 'created_at']
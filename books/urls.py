from django.urls import path
from .views import BookCreateView, BookUpdateView, BookDeleteView, BookSearchView, BookRecommendationView

urlpatterns = [
    path('add', BookCreateView.as_view(), name='add-book'),
    path('update/<int:pk>', BookUpdateView.as_view(), name='update-book'),
    path('delete/<int:pk>', BookDeleteView.as_view(), name='delete-book'),
    path('search', BookSearchView.as_view(), name='search-book'),
    path('recommendations', BookRecommendationView.as_view(), name='search-book'),
]
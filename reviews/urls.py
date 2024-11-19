from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView, BookAverageRatingView, UserReviewView, BookReviewsView

urlpatterns = [
    path('add', ReviewCreateView.as_view(), name='add-review'),
    path('update/<int:pk>', ReviewUpdateView.as_view(), name='update-review'),
    path('delete/<int:pk>', ReviewDeleteView.as_view(), name='delete-review'),
    path('average-rating/<int:pk>', BookAverageRatingView.as_view(), name='average-rating'),
    path('user-review/<int:book_id>', UserReviewView.as_view(), name='user-review'),
    path('book-reviews/<int:book_id>', BookReviewsView.as_view(), name='book-reviews'),
]
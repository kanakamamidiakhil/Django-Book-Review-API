from math import ceil

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from django.db.models import Avg

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.id
            print(request.data)
            response = super().create(request, *args, **kwargs)
            return Response({"success": "true", "data": response.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        try:
            review = self.get_object()
            request.data['user'] = request.user.id
            request.data['book'] = review.book.id
            print(request.data)
            response = super().update(request, *args, **kwargs)
            return Response({"success": "true", "data": response.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return Response({"success": "true"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookAverageRatingView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            average_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
            return Response({"success": "true", "data": {"average_rating": average_rating}}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserReviewView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        book_id = self.kwargs['book_id']
        return Review.objects.filter(user=user, book_id=book_id).order_by('-created_at').first()

    def retrieve(self, request, *args, **kwargs):
        try:
            review = self.get_object()
            serializer = self.get_serializer(review)
            return Response({"success": "true", "data": serializer.data}, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"success": "false", "error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            page_no = int(request.headers.get('page-no', 1))
            page_size = int(request.headers.get('page-size', 10))
            queryset = self.get_queryset()
            total_reviews = queryset.count()
            offset = (page_no - 1) * page_size
            paginated_queryset = queryset[offset:offset + page_size]
            serializer = self.get_serializer(paginated_queryset, many=True)
            return Response({
                "success": "true",
                "data": serializer.data,
                "total_reviews": total_reviews,
                "page_no": page_no,
                "page_size": page_size
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
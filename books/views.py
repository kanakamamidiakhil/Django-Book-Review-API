from rest_framework import generics, status
from rest_framework.response import Response
from .models import Book
from .permissions import IsAdminPasswordCorrect
from .serializers import BookSerializer
from django.db.models import Avg
from django.db.models.functions import Coalesce

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminPasswordCorrect]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({"success": "true"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminPasswordCorrect]

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response({"success": "true"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminPasswordCorrect]

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return Response({"success": "true"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        ISBN = self.request.query_params.get('ISBN', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        elif author:
            queryset = queryset.filter(author__icontains=author)
        elif ISBN:
            queryset = queryset.filter(ISBN=ISBN)
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)

        queryset = queryset.annotate(average_rating=Coalesce(Avg('review__rating'), 0.0))
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        if sort_by in ['title', 'author']:
            queryset = queryset.order_by(sort_by)
        elif sort_by in ['average_rating', 'created_at']:
            queryset = queryset.order_by('-'+sort_by)
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            page_no = int(request.headers.get('page-no', 1))
            page_size = int(request.headers.get('page-size', 10))
            queryset = self.get_queryset()
            total_books = queryset.count()
            offset = (page_no - 1) * page_size
            paginated_queryset = queryset[offset:offset + page_size]
            serializer = self.get_serializer(paginated_queryset, many=True)
            return Response({
                "success": "true",
                "data": serializer.data,
                "total_books": total_books,
                "page_no": page_no,
                "page_size": page_size
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookRecommendationView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        queryset = queryset.annotate(average_rating=Coalesce(Avg('review__rating'), 0.0))
        queryset = queryset.order_by('-average_rating')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            page_no = int(request.headers.get('page-no', 1))
            page_size = int(request.headers.get('page-size', 10))
            queryset = self.get_queryset()
            total_books = queryset.count()
            offset = (page_no - 1) * page_size
            paginated_queryset = queryset[offset:offset + page_size]
            serializer = self.get_serializer(paginated_queryset, many=True)
            return Response({
                "success": "true",
                "data": serializer.data,
                "total_books": total_books,
                "page_no": page_no,
                "page_size": page_size
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
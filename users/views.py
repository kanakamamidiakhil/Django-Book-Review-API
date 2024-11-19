
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({"success": "true"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": "false", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": "true", "data": serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({"success": "false", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
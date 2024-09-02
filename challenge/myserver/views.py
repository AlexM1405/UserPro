import logging
from django.contrib.auth.models import User
from django.utils.log import DEFAULT_LOGGING
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

logger = logging.getLogger(__name__)

class UserListCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, serializer):
        if serializer.is_valid():
            serializer.save(User=self.request.user)
        else:
            logger.error(serializer.errors)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete', 'put', 'patch']
    permission_classes = (IsAuthenticated,)
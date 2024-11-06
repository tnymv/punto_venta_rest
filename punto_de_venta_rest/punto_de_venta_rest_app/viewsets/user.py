# views.py

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from punto_de_venta_rest_app.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet para ver y editar usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Define los permisos de acceso a las diferentes acciones del ViewSet.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

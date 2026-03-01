from rest_framework import generics, permissions, viewsets
from .serializers import RegisterSerializer, SecurityLogSerializer
from .models import SecurityLog, User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] 


class SecurityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SecurityLog.objects.all().order_by('-timestamp')
    serializer_class = SecurityLogSerializer
    # ONLY ADMINS can see security logs
    permission_classes = [permissions.IsAdminUser]
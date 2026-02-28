from rest_framework import generics, permissions
from .serializers import RegisterSerializer, SecurityLogSerializer
from .models import SecurityLog

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] 


class SecurityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SecurityLog.objects.all().order_by('-timestamp')
    serializer_class = SecurityLogSerializer
    # ONLY ADMINS can see security logs
    permission_classes = [permissions.IsAdminUser]
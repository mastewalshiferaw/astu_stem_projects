from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer # (Standard ModelSerializer)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
from rest_framework import viewsets, permissions
from .models import Ticket, Category
from .serializers import TicketSerializer, CategorySerializer
from .permissions import IsOwnerOrStaff

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(author=user).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in student
        serializer.save(author=self.request.user)
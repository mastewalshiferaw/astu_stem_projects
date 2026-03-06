from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Ticket, Category, TicketRemark
from .serializers import TicketSerializer, CategorySerializer
from .permissions import IsOwnerOrStaff
from accounts.models import SecurityLog
from chatbot.models import FAQ




@extend_schema_view(
    create=extend_schema(
        operation_id="upload_ticket",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'},
                    'category': {'type': 'integer', 'description': 'ID 1 for Internet, 2 for Dorm'},
                    'attachment': {'type': 'string', 'format': 'binary'}, # FORCES FILE BUTTON
                },
                'required': ['title', 'description', 'category']
            }
        },
        responses={201: TicketSerializer}
    )
)
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    parser_classes = (MultiPartParser, FormParser) # REQUIRED FOR FILE BUTTON

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(author=user).order_by('-created_at')

    def perform_create(self, serializer):
        # ONLY ONE perform_create method allowed!
        serializer.save(author=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.role == 'STUDENT' and obj.author != self.request.user:
            SecurityLog.objects.create(
                user=self.request.user,
                action=f"UNAUTHORIZED ACCESS ATTEMPT on Ticket #{obj.id}",
                is_suspicious=True,
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
        return obj

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        if request.user.role not in ['STAFF', 'ADMIN']:
            return Response({"error": "Unauthorized"}, status=403)
        
        new_status = request.data.get('status')
        remark_text = request.data.get('remark')
        if new_status in Ticket.Status.values:
            ticket.status = new_status
            ticket.assigned_staff = request.user
            ticket.save()
            if remark_text:
                TicketRemark.objects.create(ticket=ticket, author=request.user, comment=remark_text)
            return Response({"status": "Updated"})
        return Response({"error": "Invalid status"}, status=400)

class AdminAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response({"error": "Admin access required"}, status=403)

        # CRUCIAL: Seeding the FAQ so the Chatbot has answers
        if not Category.objects.exists():
            cats = ['Internet', 'Dormitory', 'Lab', 'Classroom']
            for c in cats: Category.objects.create(name=c)
        
        # Ensure the Chatbot has the "WiFi" answer in the DB
        if not FAQ.objects.filter(question__icontains="wifi").exists():
            FAQ.objects.create(
                question="How to reset WiFi password?",
                answer="Visit the ICT office in the Red Building, Room 204.",
                category="Network"
            )

        total_tickets = Ticket.objects.count()
        data = {
            "total_complaints": total_tickets,
            "resolved_complaints": Ticket.objects.filter(status='RESOLVED').count(),
            "status_breakdown": Ticket.objects.values('status').annotate(count=Count('status'))
        }
        return Response(data)
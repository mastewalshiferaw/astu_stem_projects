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
                    'category': {'type': 'integer'},
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
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(author=user).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user
        serializer.save(author=self.request.user)

    def get_object(self):
        obj = super().get_object()
        # Security: Log suspicious access attempts
        if self.request.user.role == 'STUDENT' and obj.author != self.request.user:
            SecurityLog.objects.create(
                user=self.request.user,
                action=f"UNAUTHORIZED ACCESS ATTEMPT on Ticket #{obj.id}",
                is_suspicious=True,
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
            # Permission classes will handle the actual blocking
        return obj

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        if request.user.role not in ['STAFF', 'ADMIN']:
            return Response({"error": "Only Staff can update status"}, status=403)

        new_status = request.data.get('status')
        remark_text = request.data.get('remark')

        if new_status in Ticket.Status.values:
            ticket.status = new_status
            ticket.assigned_staff = request.user
            ticket.save()

            if remark_text:
                TicketRemark.objects.create(
                    ticket=ticket, author=request.user, comment=remark_text
                )
            return Response({"status": f"Ticket updated to {new_status}"})
        return Response({"error": "Invalid status"}, status=400)

class AdminAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response({"error": "Admin access required"}, status=403)

        # --- AUTO-SEED LOGIC (Because you can't use Shell) ---
        # If you visit this URL and the DB is empty, it fills it automatically!
        if not Category.objects.exists():
            cats = ['Internet', 'Dormitory', 'Lab', 'Classroom']
            for c in cats: Category.objects.create(name=c)
            FAQ.objects.get_or_create(question="WiFi Help", answer="Go to Red Building Room 204", category="Network")
        
        total_tickets = Ticket.objects.count()
        resolved_tickets = Ticket.objects.filter(status='RESOLVED').count()
        resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
        category_stats = Category.objects.annotate(num_tickets=Count('tickets')).order_by('-num_tickets')[:5]

        return Response({
            "total_complaints": total_tickets,
            "resolution_rate": f"{round(resolution_rate, 2)}%",
            "common_issues": [{"category": c.name, "count": c.num_tickets} for c in category_stats],
        })
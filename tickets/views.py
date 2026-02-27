from rest_framework import viewsets, permissions
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ticket, Category
from .serializers import TicketSerializer, CategorySerializer
from .permissions import IsOwnerOrStaff
from django.db.models import Count, Q
from rest_framework.views import APIView
from accounts.models import SecurityLog

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]


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


    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(author=user).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in student
        serializer.save(author=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        new_status = request.data.get('status')
        remark_text = request.data.get('remark')

        # Security check: Only staff can change status
        if request.user.role not in ['STAFF', 'ADMIN']:
            return Response({"error": "Unauthorized to change status"}, status=403)

        if new_status in Ticket.Status.values:
            ticket.status = new_status
            ticket.assigned_staff = request.user #assigned to the staff who updated it
            ticket.save()

            #  audit trail remark
            if remark_text:
                TicketRemark.objects.create(
                    ticket=ticket,
                    author=request.user,
                    comment=remark_text
                )
            return Response({"status": f"Ticket updated to {new_status}"})
        
        return Response({"error": "Invalid status"}, status=400)


#Admin need to see most common issue and resolution rate
#Django's Count and Q calculate this efficienntly

class AdminAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response({"error": "Admin access required"}, status=403)

        total_tickets = Ticket.objects.count()
        resolved_tickets = Ticket.objects.filter(status='RESOLVED').count()
        
        # Resolution Rate Logic
        resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0

        # Most common categories
        category_stats = Category.objects.annotate(
            num_tickets=Count('tickets')
        ).order_by('-num_tickets')[:5]

        data = {
            "total_complaints": total_tickets,
            "resolved_complaints": resolved_tickets,
            "resolution_rate": f"{round(resolution_rate, 2)}%",
            "common_issues": [
                {"category": c.name, "count": c.num_tickets} for c in category_stats
            ],
            "status_breakdown": Ticket.objects.values('status').annotate(count=Count('status'))
        }
        return Response(data)
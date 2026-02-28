from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Ticket, Category

User = get_user_model()

class TicketSecurityTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Internet")
        self.student1 = User.objects.create_user(username="student1", password="pass", role="STUDENT")
        self.student2 = User.objects.create_user(username="student2", password="pass", role="STUDENT")
        self.ticket = Ticket.objects.create(title="My Issue", author=self.student1, category=self.category)

    def test_student_cannot_see_others_ticket(self):
        # This test ensures student2 cannot access student1's ticket
        self.client.login(username="student2", password="pass")
        response = self.client.get(f'/api/tickets/{self.ticket.id}/')
        self.assertEqual(response.status_code, 404) 
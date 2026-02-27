from django.core.management.base import BaseCommand
from tickets.models import Category
from chatbot.models import FAQ

class Command(BaseCommand):
    help = 'Populates the DB with ASTU categories and FAQs'

    def handle(self, *args, **kwargs):
        # Seed Categories
        cats = ['Internet/Network', 'Dormitory Maintenance', 'Laboratory Equipment', 'Classroom Facilities']
        for cat in cats:
            Category.objects.get_or_create(name=cat)
        
        # Seed FAQ for Chatbot
        FAQ.objects.get_or_create(
            question="How do I reset my campus WiFi password?",
            answer="Visit the ICT office in the Red Building, Room 204, with your ID card.",
            category="Network"
        )
        FAQ.objects.get_or_create(
            question="Water is leaking in my dorm room",
            answer="Submit a 'Dormitory Maintenance' ticket immediately via this app for Block repair.",
            category="Dormitory"
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded ASTU data!'))
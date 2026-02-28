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
            answer="set with API 10.240.212.**, put any numbers instead of '**' and check the ASTU GENERAL telegram channel. You might found a lot information",
            category="Network"
        )
        FAQ.objects.get_or_create(
            question="Water is leaking in our shower",
            answer="Submit a 'Dormitory Maintenance' ticket immediately via this app for Block repair.",
            category="Dormitory"
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded ASTU data!'))
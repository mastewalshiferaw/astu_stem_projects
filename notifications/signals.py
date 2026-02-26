from django.db.models.signals import post_save
from django.dispatch import receiver
from tickets.models import Ticket
from .models import Notification

@receiver(post_save, sender=Ticket)
def create_ticket_notification(sender, instance, created, **kwargs):
    if not created:  # If the ticket was updated (not just created)
        Notification.objects.create(
            recipient=instance.author,
            ticket=instance,
            message=f"Update: Your ticket '{instance.title}' status is now {instance.status}."
        )
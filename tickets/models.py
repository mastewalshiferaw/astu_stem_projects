import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_ticket_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg', '.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file. Upload images or PDFs only.')
    if value.size > 5 * 1024 * 1024: # 5MB Limit
        raise ValidationError('File too large. Max size is 5MB.')

class Category(models.Model):
    name = models.CharField(max_length=100) #problems that might be raised
    
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_tickets')
    attachment = models.FileField(upload_to='tickets/%Y/', validators=[validate_ticket_file], null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
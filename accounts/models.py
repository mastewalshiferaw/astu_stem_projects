from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        STAFF = "STAFF", "Department Staff"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True, help_text="Relevant for Staff (e.g., ICT, Maintenance)")

    def __str__(self):
        return f"{self.username} - {self.role}"
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.STAFF,
    )

    def __str__(self):
        return f'{self.username} ({self.role})'


class Report(models.Model):
    category = models.CharField(max_length=255, blank=True, default='')
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category} - {self.author} - {self.created_at}'

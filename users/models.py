from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[
            ('member', 'Member'),
            ('admin', 'Admin'),
        ],
        default='member'
    )

    def __str__(self):
        return f"{self.username}-{self.role}-{self.id}"
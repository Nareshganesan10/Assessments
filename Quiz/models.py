from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE = (
        ('Attend Quiz', 'Attend Quiz'),
        ('Present Quiz', 'Present Quiz'),
    )

    role = models.CharField(choices=ROLE, default=False, max_length=50)

    def __str__(self):
        return self.username
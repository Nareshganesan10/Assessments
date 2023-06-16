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
    
class Quiz(models.Model):
    quiz_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    number_of_questions = models.IntegerField(null=False)
    required_score_to_pass = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.quiz_name
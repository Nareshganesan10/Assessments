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
    username = models.CharField(max_length=50)
    quiz_id = models.AutoField(primary_key=True)
    quiz_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    required_score_to_pass = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.quiz_name
    
class Questions(models.Model):
    username = models.CharField(max_length=50)
    quiz_name = models.CharField(max_length=50)
    question = models.CharField(max_length=300)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=300)

    def __str__(self):
        return self.question

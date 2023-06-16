# from quiz.models import PostModel
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from quiz.models import CustomUser

# class PostForm(ModelForm):
#     body = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'required': 'True',
#         'placeholder': 'Say anything'
#     }))

#     class Meta:
#         model = PostModel
#         fields = ['body']

role = [
        ('Attend Quiz', 'Attend Quiz'),
        ('Present Quiz', 'Present Quiz'),
    ]

class SignupForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    role = forms.CharField(label='Select your role?', widget=forms.Select(choices=role))
    username = forms.CharField(max_length=50, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = ["email", "role", "username", "password1", "password2"]
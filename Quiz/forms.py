# from quiz.models import PostModel
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from quiz.models import CustomUser

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

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("The password and Re-confirmation of the password didn't match")
        elif len(password1) < 8:
            raise forms.ValidationError("Password must have minimum of 8 character")
        if "@" not in email:
            raise forms.ValidationError("Enter a valid email id")
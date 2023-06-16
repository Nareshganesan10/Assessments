from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignupForm
from quiz.models import CustomUser, Quiz

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def home(request):
    user_role = request.user.role
    existing_quizzes_list = Quiz.objects.all()
    return render(request, "home.html",{
        'user_role': user_role,
        'existing_quizzes_list': existing_quizzes_list,
    })


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signin(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request,"Logged in")
            return redirect('home')
        else:
            messages.success(request, "incorrect username or password")
            return redirect('signin')
    return render(request, "signin.html", {
        'form': form,
    })


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            if password1 == password2:
                if CustomUser.objects.filter(email=email).exists():
                    pass
                else:
                    user = CustomUser.objects.create(username=username, password=password1, email=email, role=role)
                    user.set_password(password1)
                    user.save()
                    messages.success(request, "Account succesfully created")
                    new_user = authenticate(username=username, password=password1)
                    if new_user is not None:
                        login(request, new_user)
                        messages.success(request,"Logged in")
                        return redirect('home')
                    return redirect('signup')
        else:
            messages.success(request, form.errors)
    else:
        form = SignupForm()
        return render(request, "signup.html", {
            'form': form,
        })
    return redirect('signup')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signout(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect('signin')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def create_quiz(request):
    if request.method == 'POST':
        quiz_name = request.POST.get('quiz_name')
        category = request.POST.get('category')
        number_of_questions = request.POST.get('number_of_questions')
        required_score_to_pass = request.POST.get('required_score')
        duration = request.POST.get('duration')
        if Quiz.objects.filter(quiz_name=quiz_name).exists():
            messages.success(request, "Quiz name is already taken, Please try a new name")
            return redirect('home')
        else:
            quiz = Quiz.objects.create(quiz_name=quiz_name, category=category, number_of_questions=number_of_questions, 
                                    required_score_to_pass=required_score_to_pass, duration=duration)
            quiz.save()
            messages.success(request, "Quiz has been succesfully created")
    else:
        return redirect('home')
    return redirect('home')
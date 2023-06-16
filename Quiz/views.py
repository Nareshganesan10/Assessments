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
from quiz.models import CustomUser

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def home(request):
    # posts = PostModel.objects.all().order_by('-time_posted')
    # form = PostForm()
    # if request.method == 'GET':
    #     form = PostForm(request.GET)

    # elif request.method != 'POST':
    #     return render(request, "authenticate/home.html", {
    #         "posts": posts,
    #     })
    # elif request.method == 'POST':
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         new_post = form.save(commit=False)
    #         new_post.username = request.user
    #         new_post.save()
    #         messages.success(request, "Posted")
    #         return redirect("home")
    #     messages.success(request, "Posted")
    #     return redirect('home')
    # context = {
    #     'form': form,
    #     'posts': posts,
    # }
    return render(request, "home.html",{})


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
            messages.error(request, form.errors)
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

from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from quiz.models import CustomUser, Quiz, Questions
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore



#landing pag with the existing Quiz details
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_role = request.user.role
            existing_quizzes_list = Quiz.objects.all()
            return render(request, "home.html",{
                'user_role': user_role,
                'existing_quizzes_list': existing_quizzes_list,
                "is_authenticated": request.session.get('is_authenticated', True),
            })
        else:
            return render(request, "home.html", {
                "is_authenticated": False,
            })


#user signin
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signin(request):
    form = AuthenticationForm(request)
    print(form.errors)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()         
            login(request, user)
            is_authed = True
            user_role = request.user.role
            existing_quizzes_list = Quiz.objects.all()
            messages.success(request,"Logged in")
            response = render(request, 'home.html', {
                "is_authenticated": is_authed,
                "user_role": user_role,
                "existing_quizzes_list": existing_quizzes_list,
            })
            response.set_cookie(key='username', value=request.user)
            response.set_cookie(key='is_authenticated', value=True)
            return response
        else:
            messages.success(request, "incorrect username or password")
            return redirect('signin')
    else:
        if request.session.get("is_authenticated", False):
            messages.success(request,"Logged in")
            is_authed = True
            return render(request, "signin.html", {
                'form': form,
                "is_authenticated": is_authed,
            })
        return render(request, "signin.html", {
            'form': form,
            })


#user account ceation along with their roles (quiz_attender or quiz_presenter)
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


#user signout
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signout(request):
    logout(request)
    response = redirect('signin')
    response.set_cookie(key='username', value='logged_out')
    response.set_cookie(key='is_authenticated', value=False)
    # session_key = request.session.session_key
    # SessionStore(session_key=session_key).delete()
    # request.session.flush()
    messages.success(request,"Logged out")
    return response


#the quiz presenter is creating the Quiz details and posting it
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
            quiz = Quiz.objects.create(quiz_name=quiz_name, username=str(request.user), category=category, 
                                    required_score_to_pass=required_score_to_pass, duration=duration)
            quiz.save()
            messages.success(request, "Quiz has been succesfully created, Add you questions...")
            return redirect('home')
    return redirect('home')


#the quiz attender starts answering the questions
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def start_quiz(request, quiz_name):
    quiz_name = quiz_name
    question = Questions.objects.filter(quiz_name=quiz_name).values_list()
    return render(request, "start_quiz.html", {
        "question_list": question,
        # "number_of_question": len(question),
    })


#the quiz presenter making the question
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def add_questions(request):
    quiz_name = request.POST.get('quiz_name')
    user_role = request.user.role
    user_list = Quiz.objects.filter(username=request.user)
    for user in user_list:
        quiz_name = user.quiz_name
        print(quiz_name)
    if request.method == 'GET':
        return render(request, "add_questions.html", {
            "user_role": user_role,
            "quiz_name":quiz_name,
            })
    elif request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')
        username = CustomUser.objects.get(username=request.user)
        quiz_name = Quiz.objects.get(quiz_name=quiz_name)
        print("quiz",quiz_name.quiz_name)
        question = Questions.objects.create(username=str(username), quiz_name=quiz_name.quiz_name,
                                            question=question, option1=option1, option2=option2,
                                            option3=option3, option4=option4, correct_answer=correct_answer)
        
        question.save()
        messages.success(request, "Question have been added successfully, Add the next question")
        return render(request, "add_questions.html", {
            "user_role": user_role,
            "quiz_name":quiz_name,
            })
    return render(request, "add_questions.html", {
        "user_role": user_role,
        "quiz_name":quiz_name,
    })
from django.urls import path
from quiz import views

urlpatterns = [
    path('', view=views.home, name="home"),    
    path("signin/", view=views.signin, name="signin"),
    path("signup/", view=views.signup, name="signup"),
    path("signout/", view=views.signout, name="signout"),
    path("create_quiz/", view=views.create_quiz, name="create_quiz"),
    path("start_quiz/", view=views.start_quiz, name="start_quiz"),
    path("add_questions/", view=views.add_questions, name="add_questions"),
]

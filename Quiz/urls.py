from django.urls import path
from quiz import views

urlpatterns = [
    path('home/', view=views.home, name="home"),    
    path("signin/", view=views.signin, name="signin"),
    path("signup/", view=views.signup, name="signup"),
    path("signout/", view=views.signout, name="signout"),
]

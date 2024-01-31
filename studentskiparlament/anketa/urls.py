from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from . forms import LoginForm
from .views import PasswordsChange

urlpatterns = [
    path('home/', views.hosthomepage, name='hosthomepage'),
    path('login/', auth_views.LoginView.as_view(template_name='anketa/login.html', authentication_form=LoginForm), name="hostlogin"),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.host_logout, name='hostlogout'),
    path("change_password/", PasswordsChange.as_view(), name='passwordchange'),
    path('anketa/', views.host_makes_anketa, name='hostmakesanketa'),
    path('email/', views.success_mail, name='email')
]
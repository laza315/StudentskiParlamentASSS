from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from . forms import LoginForm, PitanjaForm
from .views import PasswordsChange

urlpatterns = [
    path('home/', views.hosthomepage, name='hosthomepage'),
    path('login/', auth_views.LoginView.as_view(template_name='anketa/login.html', authentication_form=LoginForm), name="hostlogin"),
    path('profile/', views.profile, name='profile'),
    path('mojeankete/<int:pk>/', views.user_surveys, name='mojeankete'),
    path('logout/', views.host_logout, name='hostlogout'),
    path("change_password/", views.PasswordsChange.as_view(), name='passwordchange'),
    path('anketa/', views.host_makes_anketa, name='hostmakesanketa'),
    path('email/', views.success_mail, name='email'),
    path('pitanja/<int:anketa_id>', views.definisanje_pitanja, name='pitanja'),
    path('mojeankete/details/<int:pk>', views.survay_details, name="details"),
    path('anketa/<int:anketa_id>/pitanje/<int:pitanje_id>/pregled/', views.query_za_izbor, name='pregled_ankete')
]
"""
URL configuration for studentskiparlament project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from anketa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('host_view/', include('anketa.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.available_anketas_for_students, name='available_anketas_for_students'),
    path('voter_checker/<int:anketa_id>/', views.can_students_code_vote_checker, name='code_checker'),
    path('vote/<int:anketa_id>/<int:kod_value>/', views.vote, name='vote'),

]


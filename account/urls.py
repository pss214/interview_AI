"""
URL configuration for interview_AI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# account/urls.py
from django.urls import path
from . import views

app_name = 'account'  # 'account'라는 이름공간 설정

urlpatterns = [
    path('login/', views.login_view, name='login'),  # 로그인 페이지 URL
    path('signup/', views.signup_view, name='signup'),  # 회원가입 페이지 URL
]

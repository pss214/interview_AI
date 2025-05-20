from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re  # 정규식 모듈

# 이메일 정규식 (기본적인 형식 검사)
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# 비밀번호 정규식 (예: 영문자+숫자, 8자 이상)
PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'


# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # 이메일 형식 검사
        if not re.match(EMAIL_REGEX, email):
            messages.error(request, '유효한 이메일 형식이 아닙니다.')
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('chatbot:index')
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'login.html')


# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # 이메일 형식 확인
        if not re.match(EMAIL_REGEX, email):
            messages.error(request, '유효한 이메일 형식이 아닙니다.')

        # 비밀번호 일치 여부
        elif password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')

        # 비밀번호 정규식 검사
        elif not re.match(PASSWORD_REGEX, password):
            messages.error(request, '비밀번호는 8자 이상이며, 영문자와 숫자를 포함해야 합니다.')

        else:
            try:
                user = User.objects.create_user(username=email, password=password)
                user.save()
                messages.success(request, '회원가입이 완료되었습니다. 로그인 해주세요.')
                return redirect('account:login')
            except Exception as e:
                print(e)
                messages.error(request, '회원가입에 실패했습니다. 다시 시도해주세요.')

    return render(request, 'signup.html')


# 로그아웃 뷰
def logout_view(request):
    logout(request)
    return redirect('index')
def index(request):
    return render(request,'main.html')

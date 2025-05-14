# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chatbot:index')  # 로그인 성공 후 이동할 페이지
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'login.html')

# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            # 사용자 생성
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, '회원가입이 완료되었습니다. 로그인 해주세요.')
                return redirect('login')  # 회원가입 후 로그인 페이지로 리디렉션
            except:
                messages.error(request, '회원가입에 실패했습니다. 다시 시도해주세요.')

    return render(request, 'signup.html')

# account/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # 기본 User 모델 사용

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': '사용자 이름',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

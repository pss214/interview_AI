from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # 기본 User 모델 사용

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        labels = {
            'email': '이메일',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    # 비밀번호 길이 검증 추가
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('비밀번호는 최소 8자 이상이어야 합니다.')
        return password

# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' 또는 'bot'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username} ({self.sender}): {self.message}"

    def save(self, *args, **kwargs):
        # 이메일 인증된 사용자만 메시지를 저장할 수 있도록 합니다.
        if self.user.is_verified:  # 'is_verified' 필드가 'True'일 경우만 저장
            super().save(*args, **kwargs)
        else:
            raise ValueError("이메일 인증이 완료된 사용자만 메시지를 작성할 수 있습니다.")

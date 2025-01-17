# account/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser,  Group, Permission
from django.forms import forms

## 확장 User 모델 
# - AbstractUser로 구현: 기본 User(username, password)에 필드들을 추가하는 방식
# - AbstractUser 상속. 필드들 정의(username, password빼고 정의)
class User(AbstractUser):
    
    # Field들 정의 - table컬럼
    name = models.CharField(
        verbose_name="이름", # Form관련설정(label) - Form을 ModelForm을 만들 경우 form관련설정을 Model에 한다.
        max_length=50 # varchar(50)
    )
    birthday = models.DateField(
        verbose_name="생일",
    )
    gender = models.CharField(
        verbose_name="성별",
        max_length=1,
        choices=[('M', '남성'),('F', '여성')]
    )
    groups = models.ManyToManyField(
        Group,
        related_name="account_users",  # 기본 user_set 대신 account_users 사용
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="account_users_permissions",  # 기본 user_set 대신 account_users_permissions 사용
    )
    
    
    def __str__(self):
        return f"username: {self.username}, name: {self.name}"


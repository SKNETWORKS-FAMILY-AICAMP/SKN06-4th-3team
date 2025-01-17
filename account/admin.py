# account/admin.py

from django.contrib import admin

# 사용자 정의 UserAdmin 클래스 정의
## UserAdmin은 관리자 앱에서 User의 어떤 항목들을 관리할지 정의.
## UserAdmin을 상속해서 구현. admin.site.register() 할 때 Model과 같이 등록

### class 변수로 항목들 정의
### list_display: List - admin Users의 메인화면 목록에 나올 항목(attribute)
### add_fieldsets: Tuple - 등록화면에 나올 항목들을 지정.
### fieldsets: Tuple - 수정화면에 나올 항목들을 지정.

#### field: 개별 atttibute. fieldset은 field들의 묶음(group)
### fieldset 정의하는 구조
# (
#     fieldset이름-문자열,None,
#     fieldset에 묶을 field들 지정. -> dictionary
# )

from .models import User
from django.contrib.auth.admin import UserAdmin

# admin app 에서 사용자(User)를 등록/수정/조회 하는 화면 구성성
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'name', 'email']
    add_fieldsets = (
        ("인증정보", {"fields":("username", "password1", "password2")}),
        ("개인정보", {"fields":("name", "email", "birthday")}),
        ("권한", {"fields":("is_active", "is_superuser")})
    )
    # 수정화면: password만 지정.
    fieldsets = (
        ("인증정보", {"fields":("username", "password")}), 
        ("개인정보", {"fields":("name", "email", "birthday")}),
        ("권한", {"fields":("is_active", "is_superuser")})
    )

admin.site.register(User, CustomUserAdmin)
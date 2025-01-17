# account/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import (
    login, # 로그인 처리 - 로그인사용자의 Model을 session에 저장(로그아웃할 때까지 정보유지.)
    logout,# 로그아웃 처리 - session에서 로그인사용자 Model을 제거
    authenticate, # 인증확인 - username, password DB에서 확인
    update_session_auth_hash 
    # 회원정보 수정에서 사용. 수정된 정보를 session의 User Model에 적용.

)
from django.contrib.auth.decorators import login_required


# login()/logout(): 로그인/로그아웃 처리. 
#                        - 로그인한 사용자정보를 session에 추가/제거
# authenticate(): username(id)/password를 확인하는 함수.

from django.contrib.auth.forms import (
    AuthenticationForm, # 로그인폼
    PasswordChangeForm  # 비밀번호 변경 폼
)

from .models import User
## 로그인 ModelForm (username, password 두개 필드정의-Model: User)

from .forms import CustomUserCreationForm, CustomUserChangeForm

# account/views.py

# 사용자 가입 (요청파라미터-CustomUserCreationForm-ModelForm 이용)
## 요청url:  /account/create
###  요청방식: GET - 가입 양식화면을 반환(templates/accout/create.html)
###           POST - 가입처리. 메인페이지로 이동 (templates/home.html)
def create(request):
    if request.method == "GET":
        # 가입 화면을 응답.
        ## 빈 Form객체를 Context Data로 template에 전달.
        return render(
            request, "account/create.html", {"form":CustomUserCreationForm()}
        )
    elif request.method == "POST":
        # 가입처리.
        # 1. 요청파라미터 조회. request.POST.get("name")->Form
        form = CustomUserCreationForm(request.POST, request.FILES)
        # request.POST: post방식으로 넘어온 요청파라미터들
        # request.FILES: 파일업로드시 업로드된 파일 정보.
        ## 객체 생성 -> 요청파라미터들을 attribute로 저장. 검증처리.

        # 2. 요청파라미터 검증
        if form.is_valid(): # 검증에러 없으면 True.
            # 3. DB에 저장(검증 성공)
            user = form.save() 
            print("---------create:", type(user))
            #ModelForm의 save(): Model.save()-insert/update
            #    반환 - 저장한 정보를 가지는 Model객체를 반환.
            
            ## 가입후 바로 로그인 처리.
            login(request, user) # login(request, 로그인한사용자Model)
            ## 응답페이지로 이동 - redirect 방식으로 이동.
            return redirect(reverse("home"))
        
        else: # 요청파라미터 검증 실패
            # 가입화면(create.html)으로 이동.
            return render(
                request, "account/create.html", 
                {"form":form} # form: 요청파라미터와 검증결과를 가진 form
            )

        # 4. 응답 - 성공: home.html, 실패(검증): 가입화면으로 이동

# 로그인 처리 View
## 요청 URL: /account/login
##   GET-로그인폼 페이지를 반환. POST-로그인 처리.
def user_login(request):
    if request.method == "GET":
        # 로그인 폼 페이지를 반환
        return render(
            request, "account/login.html", {"form":AuthenticationForm()}
        )
    elif request.method == "POST":
        # 로그인 처리
        # username, password 요청파라미터 조회
        username = request.POST['username']
        password = request.POST['password']

        # settings.AUTH_USER_MODEL 모델을 기반으로 사용자인증처리.
        #  username과 password가 유효한 사용자 계정이면(select) User 모델을 반환
        #                        유효하지 않은 사용자이면 None 반환환
        user = authenticate(
            request, username=username, password=password
        )
        if user is not None: # 유효한 사용자
            # 로그인처리
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))

            return redirect(reverse("home"))
        
        else: # 유효하지 않은 사용자.
            return render(
                request, "account/login.html", 
                {"form":AuthenticationForm(), 
                 "error_msg":"username이나 password를 다시 확인하세요."}
            )
    
# 로그아웃
## Login안한 상태에서 요청을 받으면 settings.LOGIN_URL 로 이동.
@login_required
def user_logout(request):
    # login() 이 처리한 것들을 모두 무효화한다.
    logout(request)
    return redirect(reverse('home'))


# 로그인한 사용자 정보 조회
# 요청 url: /account/detail
# view: user_detail
# 응답: account/detail.html
@login_required
def user_detail(request):
    # View에서 로그인한 사용자 정보를 조회 -> request.user (모델)
    user = User.objects.get(pk=request.user.pk)# 로그인 user의 pk
    return render(request, "account/detail.html", {"object":user})

# 패스워드 수정
## 요청 URL: /account/password_change
## view: password_change
##  GET: 패스워드변경 폼을 응답. (응답: password_change.html)
##  POST: 패스워드 변경 처리 (응답: /account/detail)
@login_required
def password_change(request):
    http_method = request.method
    if http_method == "GET":
        #비밀번호 변경할 user정보를 넣어 빈폼을 생성 - 기존 패스워드 확인용.
        form = PasswordChangeForm(request.user)
        return render(request, "account/password_change.html", 
                        {"form":form})
    
    elif http_method == "POST":
        # 요청파라미터(패스워드들) 조회, 검증.
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid(): # 검증 통과
            # db update
            user = form.save() # ModelForm.save(): Update/Insert한 모델객체
            # session에 저장된 user정보를 변경된 내용으로 변경. (안하면 logout)
            update_session_auth_hash(request, user)# request, 변경된user모델
            # 응답
            return redirect(reverse("account:detail"))
        else: # 검증 실패
            return render(request, "account/password_change.html",
                          {"form":form})
        
# 회원정보 수정 처리
## 요청 url: /account/update
## view: user_update
##  GET - 수정 폼을 응답 (account/update.html)
##  POST - 수정 처리   (회원정보 조회로 이동: account:detail)
@login_required
def user_update(request):
    http_method = request.method
    if http_method == "GET":
        # CustomUserChangeForm을 이용해 빈폼을 생성 
        #      - 로그인한 User객체를 넣어 생성. 입력 필드에 기존 데이터가 나와야함.
        form = CustomUserChangeForm(instance=request.user)
        return render(request, "account/update.html", {"form":form})

    elif http_method == "POST":
        # 요청파라미터 조회 +  검증 : Form
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid(): #검증 성공
            # DB에 update
            user = form.save()
            # session에 로그인 사용자정보를 갱신
            update_session_auth_hash(request, user)
            # 상세페이지로 이동
            return redirect(reverse("account:detail"))
        else: #검증실패 - update.html
            return render(
                request, "account/update.html", {"form":form}
            )
        
# 탈퇴
## 요청파라미터: /account/delete
## view: user_delete
## 응답: home 이동.
@login_required
def user_delete(request):
    # DB에서 로그인한 user를 삭제
    # user = request.user  # model
    request.user.delete()
        # 일반 데이터일 경우.
        # 삭제할 데이터의 pk를 path/요청 parameter로 받아서 조회
        # 조회한 Model을 이용해서 삭제.
        # Question삭제 
        # q = Question.objects.get(pk=pk)
        # q.delete()
    # 삭제후 로그아웃
    logout(request)
    return redirect(reverse('home'))


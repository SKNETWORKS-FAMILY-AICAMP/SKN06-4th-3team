from django.urls import path
from .views import  chat_message
from . import views  # ✅ api.views 확인

urlpatterns = [
    path('chat_message/<str:message>/', views.chat_message, name="chat_message"),
    path('chat_history/', views.chat_history, name="chat_history"),  # 대화 기록 불러오기
]
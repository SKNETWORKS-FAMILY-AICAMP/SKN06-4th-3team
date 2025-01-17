from django.urls import path
from .views import  chat_message
from . import views  # ✅ api.views 확인

app_name = "api"

urlpatterns = [
    path('chat_message/<str:message>/', views.chat_message, name="chat_message"),
]
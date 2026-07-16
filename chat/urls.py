from django.urls import path
from django.contrib.auth import views as auth_views
from .views import chat_room, register

urlpatterns = [
    path('', chat_room, name='chat_room'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('register/', register, name='register'),
]
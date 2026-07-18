from django.urls import path
from . import views

urlpatterns = [
    # ... ваші інші url (реєстрація, чат)
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
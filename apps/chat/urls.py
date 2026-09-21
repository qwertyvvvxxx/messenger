from django.urls import path
from .views import chat_room, chat_list, user_search, start_chat, private_chat_room

urlpatterns = [
    path('global/', chat_room, name='global_chat'),
    path('', chat_list, name='chat_list'),
    path('search/', user_search, name='user_search'),
    path('start/<str:username>/', start_chat, name='start_chat'),
    path('<int:thread_id>/', private_chat_room, name='private_chat_room')
]
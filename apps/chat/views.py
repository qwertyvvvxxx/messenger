from django.contrib.auth import get_user_model
from django.db.models import Max, OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Thread


@login_required
def chat_room(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(user=request.user, text=text)
            return redirect('global_chat')

    messages = Message.objects.filter(thread__isnull=True).select_related('user', 'user__profile')
    return render(request, 'chat/room.html', {'messages': messages})


User = get_user_model()


@login_required
def chat_list(request):
    """Оптимізований список чатів (1 запит на треди + 1 запит на учасників + 1 запит на повідомлення)"""

    threads = Thread.objects.filter(participants=request.user).prefetch_related(
        'participants',
        'messages'
    ).annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time', '-updated_at')

    chat_data = []
    for thread in threads:
        recipient = thread.get_recipient(request.user)
        messages = list(thread.messages.all())
        last_message = messages[-1] if messages else None

        chat_data.append({
            'thread': thread,
            'recipient': recipient,
            'last_message': last_message,
        })

    return render(request, 'chat/chat_list.html', {'chats': chat_data})


@login_required
def user_search(request):
    """Пошук користувачів для початку нового діалогу"""
    query = request.GET.get('q', '').strip()
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    return render(request, 'chat/user_search.html', {'users': users, 'query': query})


@login_required
def start_chat(request, username):
    """Створення або перенаправлення до існуючого чату за username"""
    recipient = get_object_or_404(User, username=username)
    if recipient == request.user:
        return redirect('chat_list')

    thread = Thread.get_or_create_between(request.user, recipient)
    return redirect('private_chat_room', thread_id=thread.id)


@login_required
def private_chat_room(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
    recipient = thread.get_recipient(request.user)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            # Використовуємо user=request.user замість sender=request.user
            Message.objects.create(thread=thread, user=request.user, text=text)
            thread.save()
            return redirect('private_chat_room', thread_id=thread.id)

    messages = thread.messages.all()
    return render(request, 'chat/private_room.html', {
        'thread': thread,
        'recipient': recipient,
        'messages': messages
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from .models import Message


@login_required
def chat_room(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(user=request.user, text=text)
            return redirect('chat_room')

    messages = Message.objects.order_by('timestamp')[:50]
    return render(request, 'chat/room.html', {'messages': messages})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('chat_room')
    else:
        form = UserCreationForm()

    return render(request, 'chat/register.html', {'form': form})

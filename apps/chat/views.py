from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

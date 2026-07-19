from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('chat_room')
    else:
        form = UserCreationForm()
        if 'username' in form.fields:
            form.fields['username'].widget.attrs.pop('autofocus', None)

    return render(request, 'register/register.html', {'form': form})

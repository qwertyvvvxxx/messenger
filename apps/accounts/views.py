from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from apps.accounts.forms import CustomUserCreationForm
from apps.accounts.models import User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('chat_room')
    else:
        form = CustomUserCreationForm()
        if 'username' in form.fields:
            form.fields['username'].widget.attrs.pop('autofocus', None)

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request, username):
    user_object = get_object_or_404(User, username=username)

    return render(request, 'accounts/profile.html', {'user_object': user_object})

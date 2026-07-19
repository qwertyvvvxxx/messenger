from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def profile_view(request, username):
    user_object = get_object_or_404(User, username=username)

    return render(request, 'profile/profile.html', {'user_object': user_object})

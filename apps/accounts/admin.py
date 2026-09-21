from django.contrib import admin

from apps.accounts.models import Profile, User

admin.site.register(Profile)
admin.site.register(User)
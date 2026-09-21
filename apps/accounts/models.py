from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='username')
    nickname = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="nickname",
    )

    def get_display_name(self):
        return self.nickname if self.nickname else self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="user")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="avatar")
    birth_date = models.DateField(null=True, blank=True, verbose_name="bith date")

    def __str__(self):
        return f"User profile {self.user.username}"

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Безпечне збереження існуючого профілю
        if hasattr(instance, 'profile'):
            instance.profile.save()
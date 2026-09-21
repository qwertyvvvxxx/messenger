from django.db import models
from django.conf import settings


class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='reads'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thread {self.id}"
    @classmethod
    def get_or_create_between(cls, user1, user2):
        if user1 == user2:
            return  None

        treads = cls.objects.filter(participants=user1).filter(participants=user2)
        if treads.exists():
            return treads[0]

        tread = cls.objects.create()
        tread.participants.add(user1, user2)

        return tread

    def get_recipient(self, current_user):
        """Повертає співрозмовника для поточного користувача"""
        return self.participants.exclude(id=current_user.id).first()


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='messages'
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_messages'
    )

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender_name = self.sender.username if self.sender else "Deleted User"
        return f"{sender_name}: {self.text[:20]}"


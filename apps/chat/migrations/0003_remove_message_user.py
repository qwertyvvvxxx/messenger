# Спершу переносимо дані з `user` у `sender`, потім видаляємо `user`.
#
# Чому два кроки в одній міграції: якщо просто видалити поле,
# усі старі повідомлення втратять автора і стануть «Видалений користувач».

from django.db import migrations, models


def copy_user_to_sender(apps, schema_editor):
    """Копіює автора з `user` у `sender`, якщо в `sender` ще порожньо."""
    Message = apps.get_model('chat', 'Message')
    Message.objects.filter(sender__isnull=True).exclude(
        user__isnull=True
    ).update(sender=models.F('user'))


def nothing_to_undo(apps, schema_editor):
    # Зворотний крок: `user` не відновлюємо, бо `sender` вже містить дані.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_options_message_sender_thread_and_more'),
    ]

    operations = [
        migrations.RunPython(copy_user_to_sender, nothing_to_undo),
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
    ]

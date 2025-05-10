from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

User = settings.AUTH_USER_MODEL  # Используем кастомную модель пользователя

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Создает или обновляет профиль пользователя при сохранении модели User.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Безопасное обновление без рекурсии
        if hasattr(instance, 'profile'):
            instance.profile.save()

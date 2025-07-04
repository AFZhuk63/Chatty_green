# posts/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from ads.models import Advertisement

from posts.templatetags import time_filters
from django.contrib.auth import get_user_model
from unidecode import unidecode
import uuid
from django.utils.timezone import now


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)  # Дата публикации
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    is_archived = models.BooleanField(default=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)  # Рекламный блок


    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = unidecode(self.title)  # Конвертируем кириллицу в латиницу
            slug = slugify(transliterated_title)  # Генерируем slug
            slug = slug[:45]  # Обрезаем для корректности
            counter = 1
            original_slug = slug
            while Post.objects.filter(slug=slug).exists():
                suffix = f"-{counter}"
                slug = f"{original_slug[:45 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['created_at']



class Advertisement(models.Model):
    title = models.CharField(max_length=255)  # Заголовок рекламы
    description = models.TextField()  # Описание рекламного объявления
    image = models.ImageField(upload_to='ads_images/', null=True, blank=True)  # Картинка рекламы
    link = models.URLField()  # Ссылка на рекламируемый ресурс
    created_at = models.DateTimeField(auto_now_add=True)  # Дата публикации рекламы
    is_active = models.BooleanField(default=True)  # Активное объявление или нет

    def __str__(self):
        return self.title

# videopost/models.py

from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from unidecode import unidecode
from ads.models import Advertisement

User = get_user_model()


# ВНЕ КЛАССА: Функция генерации уникального slug
def generate_unique_slug(instance, title, slug_field='slug', max_length=45):
    transliterated_title = unidecode(title)
    slug = slugify(transliterated_title)[:max_length]
    original_slug = slug
    ModelClass = instance.__class__
    counter = 1
    while ModelClass.objects.filter(**{slug_field: slug}).exists():
        suffix = f"-{counter}"
        slug = f"{original_slug[:max_length - len(suffix)]}{suffix}"
        counter += 1
    return slug


class VideoPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # Ссылка на видео
    thumbnail = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_videos', blank=True)
    is_archived = models.BooleanField(default=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('videopost:videopost_detail', kwargs={'slug': self.slug})


class VideoComment(models.Model):
    post = models.ForeignKey(VideoPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['created_at']

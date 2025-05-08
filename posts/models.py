from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # ✅ ЭТО ОБЯЗАТЕЛЬНО
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title[:50])
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username} — {self.title}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    text = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(default=timezone.now)  # Дата и время создания
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Привязка к посту
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Привязка к пользователю

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
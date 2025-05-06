from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username} on {self.publication_date}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

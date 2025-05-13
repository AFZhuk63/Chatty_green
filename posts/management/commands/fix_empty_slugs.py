from django.core.management.base import BaseCommand
from posts.models import Post
from django.utils.text import slugify  # или from slugify import slugify, если используешь стороннюю библиотеку

class Command(BaseCommand):
    help = 'Генерирует slug для всех постов, у которых он не задан'

    def handle(self, *args, **kwargs):
        updated = 0
        for post in Post.objects.filter(slug=''):
            base_slug = slugify(post.title or 'post')
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=post.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            post.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Обновлено {updated} постов с пустыми slug'))

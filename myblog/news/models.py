from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """Создание конкретно-прикладного менеджера, чтобы извлекать все посты,
        имеющие статус PUBLISHED. Используя обозначение Post.published.all()"""

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=37)
    slug = models.SlugField(
        max_length=37, unique_for_date='publish')  # Слаг – это короткая метка, содержащая только буквы, цифры, знаки подчеркивания или дефисы.
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='news_posts')
    body = models.TextField()
    publish = models.DateTimeField(
        default=timezone.now)  # Метод timezone.now возвращает текущую дату/время в формате, зависящем от часового пояса
    created = models.DateTimeField(
        auto_now_add=True)  # параметр auto_now_add дата будет сохраняться автоматически во время создания объекта
    updated = models.DateTimeField(
        auto_now=True)  # параметр auto_now дата будет обновляться автоматически во время сохранения объекта
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=24)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment bt {self.name} on {self.post}'
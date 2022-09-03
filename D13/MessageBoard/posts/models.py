from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django_ckeditor_5.fields import CKEditor5Field


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    category = models.ManyToManyField(Category, through='PostCategory')

    title = models.CharField(max_length=150)

    content = CKEditor5Field(config_name='extends')

    def preview(self):
        return self.content[0:123] + '...'

    def __str__(self):
        return f'"{self.title}"  (автор: {self.author.user.get_username()})'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу новости
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    approval = models.BooleanField(default=False)

    def approve(self):
        self.approval = True
        self.save()

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу поста
        return f'/posts/{self.post.id}'

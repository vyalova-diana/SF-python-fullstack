from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):

        rating_articles = self.post_set.aggregate(rating_sum=Sum('rating'))['rating_sum']
        rating_comments = self.user.comment_set.aggregate(rating_sum=Sum('rating'))['rating_sum']
        rating_feedback = self.post_set.aggregate(rating_sum=Sum('comment__rating'))['rating_sum']

        self.rating = rating_articles * 3 + rating_comments + rating_feedback
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPE_CHOICES = [
        (NEWS, 'news'),
        (ARTICLE, 'article')
    ]
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NEWS)

    date = models.DateTimeField(auto_now_add=True)

    category = models.ManyToManyField(Category, through='PostCategory')

    title = models.CharField(max_length=150)

    content = models.TextField()

    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[0:123] + '...'

    def __str__(self):
        return f'"{self.title}"  (автор: {self.author.user.get_username()})'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу новости
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    commentator = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



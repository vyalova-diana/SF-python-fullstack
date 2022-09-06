from django.db import models
from django.core.cache import cache
from django_ckeditor_5.fields import CKEditor5Field


class News(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=150)

    content = CKEditor5Field(config_name='extends')

    def preview(self):
        return self.content[0:123] + '...'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'news-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

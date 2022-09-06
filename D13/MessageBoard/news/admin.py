from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date',)


admin.site.register(News, NewsAdmin)

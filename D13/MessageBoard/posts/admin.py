from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

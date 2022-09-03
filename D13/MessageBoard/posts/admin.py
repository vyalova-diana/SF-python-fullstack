from django.contrib import admin

from .models import *
from django import forms
from django.contrib import admin as admin_module


# class PostAdminForm(forms.ModelForm):
#
#     class Meta:
#         model = Post
#         fields = ['category', 'author','title','content']


class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    list_display = ('title', 'author', 'date')
    # filter_horizontal = ['category']


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

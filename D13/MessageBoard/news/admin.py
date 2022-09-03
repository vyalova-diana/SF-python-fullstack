from django.contrib import admin
from .models import *

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


# class NewsAdminForm(forms.ModelForm):
#
#     class Meta:
#         model = News
#         fields = ['title']
#         widgets = {
#             'content': CKEditor5Widget(
#                 attrs={"class": "django_ckeditor_5"}, config_name='extends'
#             )
#         }


class NewsAdmin(admin.ModelAdmin):
    # form = NewsAdminForm
    list_display = ('title', 'date',)


admin.site.register(News, NewsAdmin)

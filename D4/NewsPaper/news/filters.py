from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms.widgets import DateInput


class NewsFilter(FilterSet):
    date = DateFilter(lookup_expr='date__gt', label='Опубликовано после ',
                              widget=DateInput(format='%d.%m.%Y"', attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'author__user__username': ['iexact'],
            'title': ['icontains']
        }

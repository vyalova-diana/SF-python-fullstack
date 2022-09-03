from django_filters import FilterSet, DateFilter
from posts.models import Post
from django.forms.widgets import DateInput


class PostsFilter(FilterSet):
    date = DateFilter(lookup_expr='date__gt', label='Опубликовано после ',
                      widget=DateInput(format='%d.%m.%Y"', attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['iexact']
        }
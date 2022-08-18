from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter
from .models import Post, Category
from django.forms.widgets import DateInput, CheckboxSelectMultiple


class NewsFilter(FilterSet):
    date = DateFilter(lookup_expr='date__gt', label='Опубликовано после ',
                              widget=DateInput(format='%d.%m.%Y"', attrs={'type': 'date'}))

    category = ModelMultipleChoiceFilter(
        field_name='category__name', queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = {
            'author__user__username': ['iexact'],
            'title': ['icontains'],
        }

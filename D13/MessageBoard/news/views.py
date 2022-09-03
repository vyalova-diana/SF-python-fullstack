from django.views.generic import ListView, DetailView
from django.core.cache import cache

from .models import News


class NewsList(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = News.objects.order_by('-date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['username'] = self.request.user.get_username()
        return context


class NewsDetail(DetailView):
    template_name = 'news/news_detail.html'
    queryset = News.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)

        return obj
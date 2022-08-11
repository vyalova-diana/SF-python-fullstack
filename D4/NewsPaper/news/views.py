from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .filters import NewsFilter


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type='NW').order_by('-date')
    paginate_by = 10


class NewsListSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type='NW').order_by('-date')
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        news_filter = NewsFilter(self.request.GET, queryset=self.get_queryset())

        paginator = Paginator(news_filter.qs, self.paginate_by) #пагинация вручную

        page = self.request.GET.get('page')
        try:    #есть ли такая страница?
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        context["filter"] = news_filter
        context["paginated_response"] = response

        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'newsDetail'
    queryset = Post.objects.filter(type='NW')

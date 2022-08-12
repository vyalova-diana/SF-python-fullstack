from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .filters import NewsFilter
from .forms import PostForm


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

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        news_filter = NewsFilter(self.request.GET, queryset=self.get_queryset())

        paginator = Paginator(news_filter.qs, self.paginate_by)  # пагинация вручную

        page = self.request.GET.get('page')
        try:  # есть ли такая страница?
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        context["filter"] = news_filter
        context["paginated_response"] = response

        return context


class NewsDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.filter(type='NW')


class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class NewsEditView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте. в шаблоне переменная object.
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.filter(type='NW')
    success_url = '/news/'

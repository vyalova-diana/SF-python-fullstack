from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post, Category
from .filters import NewsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type='NW').order_by('-date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['username'] = self.request.user.get_username()
        return context


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

        chosen_cat_pk = self.request.GET.getlist('category', default=None)
        if chosen_cat_pk:
            context['chosen_categories'] = Category.objects.filter(pk__in=chosen_cat_pk)

        return context


class NewsDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.filter(type='NW')


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = 'news.add_post'


class NewsEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = 'news.change_post'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте. в шаблоне переменная object.
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(LoginRequiredMixin,  DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.filter(type='NW')
    success_url = '/news/'
    permission_required = 'news.delete_post'

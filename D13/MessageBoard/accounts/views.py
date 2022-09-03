from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from posts.models import Author, Post
from .filters import PostsFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)

    return redirect('/')


class PostsListSearch(ListView):
    model = Post
    template_name = 'account/personal_posts_search.html'
    context_object_name = 'posts'
    # queryset = Post.objects.filter(author_user=self.request.user).order_by('-date')
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(author_user=self.request.user).order_by('-date')

        return queryset

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у
        # наследуемого класса
        context = super().get_context_data(**kwargs)
        posts_filter = PostsFilter(self.request.GET, queryset=self.get_queryset())

        paginator = Paginator(posts_filter.qs, self.paginate_by)  # пагинация вручную

        page = self.request.GET.get('page')
        try:  # есть ли такая страница?
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        context["filter"] = posts_filter
        context["paginated_response"] = response

        return context


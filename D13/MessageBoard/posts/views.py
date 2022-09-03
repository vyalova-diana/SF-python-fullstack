from django.http import Http404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import date
from django.core.cache import cache

from .models import Post, Category, Author, Comment
from .filters import PostsFilter
from .forms import PostForm, CommentForm


class PostsList(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        # context['username'] = self.request.user.get_username()
        return context


class PostsCategoryList(PostsList):
    def get_queryset(self):
        return self.queryset.filter(category=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['category'] = Category.objects.get(pk=category_id)
        if self.request.user.is_authenticated:
            context['is_not_subscribed'] = category_id not in self.request.user.category_set.values_list('id',
                                                                                                         flat=True)
        else:
            context['is_not_subscribed'] = True

        return context


@login_required
def category_subscribe(request, pk: int):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user)
    return redirect(f'/posts/category/{pk}')


class PostsListSearch(ListView):
    model = Post
    template_name = 'posts/posts_search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date')
    paginate_by = 10

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


class PostDetail(DetailView):
    template_name = 'posts/post_detail.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['comments'] = post.comment_set.filter(approval=True)

        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm
    permission_required = 'posts.add_post'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)  # Sets current user in Author field
        # limit = Post.objects.filter(date__date=date.today(), author=post.author).count()
        return super(PostCreateView, self).form_valid(form)


class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm
    permission_required = 'posts.change_post'

    # Метод get_object мы используем вместо queryset, чтобы получить информацию об объекте. в шаблоне переменная object.
    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'posts/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/accounts/profile/posts/'
    permission_required = 'posts.delete_post'


class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'posts/comment_create.html'
    form_class = CommentForm
    permission_required = 'comments.add_comment'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        comment = form.save(commit=False)
        comment.user = self.request.user
        print(comment.user)
        comment.post = Post.objects.get(pk=self.kwargs.get('pk'))
        print(comment.post)
        return super(CommentCreateView, self).form_valid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/comment_delete.html'
    queryset = Comment.objects.all()
    # success_url = '/accounts/profile/posts/'
    permission_required = 'comments.delete_comment'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        post = self.kwargs['pk_post']
        comment = self.kwargs['pk_comment']

        queryset = Comment.objects.get(post_id=post, id=comment)

        context = {'post_id': post, 'comment_id': comment}
        return queryset

    def get_success_url(self): #FIX
        previous = self.request.META.get('HTTP_REFERER')
        return redirect(previous)

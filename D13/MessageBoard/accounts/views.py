from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.account.views import ConfirmEmailView
from django.urls import reverse

from posts.models import Author, Post
from .models import OneTimeCode
from .filters import PostsFilter

from django.db.models import Prefetch

class ConfirmEmailView(ConfirmEmailView):
    """
    Override account.views.ConfirmEmailView
    """

    def post(self, *args, **kwargs):
        otp = self.request.POST['otp']

        if OneTimeCode.objects.filter(user__pk=self.get_object().email_address.user_id, code=otp).exists():
            OneTimeCode.objects.filter(code=otp).delete()
            return super().post(self, *args, **kwargs)
        else:
            User.objects.get(pk=self.get_object().email_address.user_id).delete()
            redirect_url = self.get_redirect_url()
            if not redirect_url:
                ctx = self.get_context_data()
                return self.render_to_response(ctx)
            return redirect(redirect_url)


confirm_email = ConfirmEmailView.as_view()


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='Authors')
    if not user.groups.filter(name='Authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)

    return redirect('/')


class PostsListSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'account/personal_posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(author__user=self.request.user) \
                               .prefetch_related('comment_set', 'category').order_by('-date')

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

from django.urls import path
from .views import *
from .views import category_subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view()),  # posts/
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('category/<int:pk>/', PostsCategoryList.as_view(), name='posts_category'),
    path('category/<int:pk>/subscribe/', category_subscribe, name='category_subscribe'),
    path('search/', PostsListSearch.as_view(), name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/comment/add/', CommentCreateView.as_view(), name='comment_create'),
    path('<int:pk_post>/comment/<int:pk_comment>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
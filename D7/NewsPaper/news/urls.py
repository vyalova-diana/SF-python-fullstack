from django.urls import path
from .views import NewsList, NewsDetail, NewsListSearch, PostCreateView, NewsEditView, NewsDeleteView, \
    NewsCategoryList
from .views import category_subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60 * 1)(NewsList.as_view())),  # news/
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('category/<int:pk>/', cache_page(60 * 1)(NewsCategoryList.as_view()), name='news_category'),
    path('category/<int:pk>/subscribe/', category_subscribe, name='category_subscribe'),
    path('search/', cache_page(60 * 1)(NewsListSearch.as_view()), name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete')
]

from django.urls import path
from .views import NewsList, NewsDetail
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60 * 1)(NewsList.as_view())),  # posts/
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
]
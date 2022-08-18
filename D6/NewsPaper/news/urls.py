from django.urls import path
from .views import NewsList, NewsDetail, NewsListSearch, PostCreateView, NewsEditView, NewsDeleteView

urlpatterns = [
    path('', NewsList.as_view()), #news/
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsListSearch.as_view(), name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete')
]

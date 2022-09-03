from django.urls import path
from .views import AccountView, PostsListSearch
from .views import upgrade_me

urlpatterns = [
    path('', AccountView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('posts/', PostsListSearch.as_view(), name='posts'),
]
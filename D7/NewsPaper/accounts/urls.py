from django.urls import path
from .views import AccountView
from .views import upgrade_me

urlpatterns = [
    path('', AccountView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),

]

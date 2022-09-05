"""MessageBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import AccountView
from accounts.views import confirm_email


urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('news/', include('news.urls')),
    re_path(r"^accounts/confirm-email/(?P<key>[-:\w]+)/$", view=confirm_email),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', include('accounts.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



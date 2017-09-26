from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from .views import index

from .views import AddPost, CreateAuthorView



urlpatterns = [
  url(r'^$', auth_views.login, name='login'),
  url(r'^login/$', auth_views.login, name='login'),
  url(r'^logout/$', auth_views.logout, name='logout'),
  # url(r'^flash/', include('flash.urls')),
  url(r'^accounts/login/$', auth_views.LoginView.as_view()),
  url(r'^flash/$', index, name='index'),
  url(r'^create/', AddPost, name="AddPost"),
  url(r'^signup/', CreateAuthorView.as_view(), name="CreateAuthorView"),



]
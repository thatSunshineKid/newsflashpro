from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from .views import index

from .views import PostCreate, CreateAuthorView



urlpatterns = [
  url(r'^$', index, name='index'),
  url(r'^create/', PostCreate.as_view(), name="PostCreate"),
  url(r'^signup/', CreateAuthorView.as_view(), name="CreateAuthorView")



]
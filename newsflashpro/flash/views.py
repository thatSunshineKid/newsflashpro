from django.shortcuts import render
from django.views import generic

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from .models import Author, Post


@login_required()
def index(request):
  current_user = request.user.author




  return render(
        request,
        'index.html',
        context={'current_user':current_user},
    )



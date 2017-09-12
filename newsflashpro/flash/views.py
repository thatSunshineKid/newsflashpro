from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .forms import CreateAuthorForm

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from .models import Author, Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


@login_required()
def index(request):
  current_user = request.user.author




  return render(
        request,
        'index.html',
        context={'current_user':current_user},
    )


class CreateAuthorView( SuccessMessageMixin, CreateView):
    # login_url = reverse_lazy('users:login')
    form_class = CreateAuthorForm
    template_name = 'flash/author_form.html'
    success_message = 'new user profile has been created!\nPlease login with your new username and password below.'
    success_url = '/login/'


    def get_context_data(self, **kwargs):
        context = super(CreateAuthorView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # print('user is already loggedd in.')
            messages.info(request, "Looks like you are already logged in, %s! No need for a new account." % self.request.user.username, extra_tags='alert alert-info')
            return render(request, 'index.html',{'current_user':self.request.user.author})
        else:
            form_class = CreateAuthorForm
            return render(request, 'flash/author_form.html',{'form': form_class})




    def form_valid(self, form):
        # take this code, find the right method, and

        c = {'form': form, }
        user = form.save(commit=False)
        # Cleaned(normalized) data
        phone_number = form.cleaned_data['phone_number']
        # date_of_birth = form.cleaned_data['date_of_birth']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            messages.error(self.request, "Passwords do not Match", extra_tags='alert alert-danger')
            return render(self.request, self.template_name, c)
        user.set_password(password)
        user.save()

        # Create UserProfile model
        author = Author.objects.create(user=user, phone_number=phone_number)


        return super(CreateAuthorView, self).form_valid(form)



#TODO: create forms.py file under flash. in this forms file, define a createclass from
# the Post create view here, that has an init function that sets the self.request.user.author.
#you might have to use a mixin such as loginrequiredmixin so that there's always a author object before the page is loaded.
class AuthorCreate(CreateView):
    model= Author


class PostCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post
    fields = ['title','author','url']
    success_url = '/flash'





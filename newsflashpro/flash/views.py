from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CreateAuthorForm, CreatePostForm

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Author, Post, Source

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


@login_required()
def index(request):
  current_user = request.user.author
  posts = Post.objects.all()




  return render(
        request,
        'index.html',
        context={'current_user':current_user, 'posts': posts},
    )

def about(request):
    return render(
        request,
        'about.html',
        context={'your': Mom },
    )


class CreateAuthorView( SuccessMessageMixin, CreateView):
    # login_url = reverse_lazy('users:login')
    form_class = CreateAuthorForm
    template_name = 'flash/author_form.html'
    # success_message = 'new user profile has been created!\nPlease login with your new username and password below.'
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
        if author:
            messages.success(self.request, "Welcome, %s! Please sign in with your password below." % user.username, extra_tags='success alert-success' )

        return super(CreateAuthorView, self).form_valid(form)



#TODO: create forms.py file under flash. in this forms file, define a createclass from
# the Post create view here, that has an init function that sets the self.request.user.author.
#you might have to use a mixin such as loginrequiredmixin so that there's always a author object before the page is loaded.
class AuthorCreate(CreateView):
    model= Author

# other attempt at creating post, was dumb to try and use Class here. Classes aren't as flexible dummy.
# class PostCreate(LoginRequiredMixin, CreateView):
#     login_url = '/login'
#     permission_denied_message = "Sorry, you must login to your account first to Post."
#     # model = Post
#     form_class = CreatePostForm
#     template_name = 'flash/post_form.html'
#     success_url = '/flash'

#     def get_context_data(self, **kwargs):
#         context = super(PostCreate, self).get_context_data(**kwargs)
#         context['request'] = self.request
#         context['form'] = self.get_form()
#         return context

#     def get(self, request, *args, **kwargs):
#         user = self.request.user
#         form_class = CreatePostForm
#         return render(request, 'flash/post_form.html',{'form': form_class, 'user': user})
#     #todo write POST method that populates the author and source fields

#     def post(self, request, *args, **kwargs):
#         waffle = request.POST['url']
#         source = waffle.split("/")
#         if source[2]:
#             url_source = source[2]
#         else:
#             url_source = source[0]
#         try:
#             match = Source.objects.get(base_url=url_source)
#         except Source.DoesNotExist:
#             match = None
#         if match:
#             add_source = match
#         else:
#             add_source = Source.objects.create(base_url=url_source, title=url_source)
#         request.POST._mutable = True

#         request.POST['source'] = add_source

#         return super(PostCreate, self).post(request, *args, **kwargs)


#         # FUCKKKK MEEEE  okay next step is to write a function based view instead of a class based view.
#         # use get to grab author, use post to get source of article, and save them mofos.


@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class AddPost(View):
    """ Class based view to allow for interaction with authored posts """
    def get(self, request):
        """Method to return CreatePostFom to the user
            Args:
                request <obj>: HTTP request object
            Returns:
                HTTP response with form and template variables
        """

        author = request.user.author
        form = CreatePostForm()
        return render(
            request,
            'flash/post_form.html',
            {'form': form, 'author': author}
        )

    def post(self, request):
        """Method to create authored posts
            Args:
                request <obj>: HTTP request object
            Returns:
                HTTP response(200)
                HTTP redirect(302)
        """
        author = request.user.author
        form = CreatePostForm(request.POST)
        if form.is_valid():
            new_s = form.cleaned_data['url']
            get_s = new_s.split("/")
            if get_s[2]:
                got_s = get_s[2]
            else:
                got_s = get_s[0]
            try:
                source = Source.objects.get(base_url=got_s)
            except Source.DoesNotExist:
                source = None
            if source:
                valid_s = source
            else:
                valid_s = Source.objects.create(base_url=got_s, title=got_s)
            Poster = Post.objects.create(
                author=author,
                title=form.cleaned_data['title'],
                url=new_s,
                source=valid_s
            )
            if Poster:
                messages.success(
                    request,
                    "Your Post has been added %s!" % author,
                    extra_tags='success alert-success'
                )
                return HttpResponseRedirect('/flash/')
        else:
            messages.error(
                request,
                "something went wrong, check logs",
                extra_tags='danger alert-danger'
            )
            return render(
                request,
                'flash/post_form.html',
                {'form': form, 'author': author}
            )


@login_required()
def ProfileView(request):
  current_user = request.user.author
  posts = Post.objects.filter(author_id=current_user.id)
  phone_number = current_user.phone_number


  return render(
        request,
        'flash/ProfileView.html',
        context={'current_user':current_user, 'posts': posts, 'phone_number':phone_number},
    )











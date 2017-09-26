from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Author, Post, Source

class CreateAuthorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    # Here we add the extra form fields that we will use to create another model object
    phone_number = forms.CharField(required=False)


    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
    ]

    def __init__(self, *args, **kwargs):
        super(CreateAuthorForm, self).__init__(*args, **kwargs)



class CreatePostForm(forms.Form):
    title = forms.CharField(required=True)
    url = forms.URLField(required=True)
    # author = forms.CharField(required=False)
    # source = forms.CharField(required=False)
    # write custom html form that takes get arguments and populates them in the html template.




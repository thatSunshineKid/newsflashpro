from django.db import models

from django.contrib.auth.models import User

from django.urls import reverse #Used to generate URLs by reversing the URL patterns
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # dont think we need these because User model already has them
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=10)


    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return '%s %s' % (self.user.first_name, self.user.last_name) #check out how we get the first and last name here - use this in context with displaying user info


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    url = models.URLField(max_length=1000)
    source = models.ForeignKey('Source', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         ordering = ['-created_at']

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title


    def get_absolute_url(self):
        """
        Returns the url to access a particular post instance.
        """
        return reverse('post-detail', args=[str(self.id)])


class Source(models.Model):
    base_url = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        """
        String representing the source object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular post instance.
        """
        return reverse('source-detail', args=[str(self.id)])




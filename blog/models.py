from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch.dispatcher import receiver
from django.urls import reverse
from tinymce import HTMLField
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login, social_account_added


from PIL import Image
import requests


User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(
        User, related_name='author', on_delete=models.CASCADE, auto_created=True)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category, related_name='post')
    featured = models.BooleanField(default=True)
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail-post', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('update-post', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('delete-post', kwargs={
            'id': self.id
        })

    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.user.username


@receiver(user_signed_up)
def set_initial_user_names(request, user=User, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more in the 'extra_data' field.

    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    preferred_avatar_size_pixels = 256

    if sociallogin:

        if sociallogin.account.provider == 'facebook':
            # verified = sociallogin.account.extra_data['verified']
            picture_url = sociallogin.account.get_avatar_url()
            im = Image.open(requests.get(picture_url, stream=True).raw)

            author = Author()
            author.user = user
            author.profile_picture = im.show()
            author.save()

        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name = sociallogin.account.extra_data['family_name']
            # verified = sociallogin.account.extra_data['verified_email']
            picture_url = sociallogin.account.extra_data['picture']
    print('ADDED')

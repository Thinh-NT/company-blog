from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.core.files import File
from django.dispatch.dispatcher import receiver
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

from urllib.request import urlopen
from tempfile import NamedTemporaryFile

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(
        User, related_name='author', on_delete=models.CASCADE, auto_created=True)
    profile_picture = models.ImageField()
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


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
def set_initial_user_names(request, user=None, sociallogin=None, **kwargs):
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

    if user == None:
        user = User

    if sociallogin:

        if sociallogin.account.provider == 'facebook':
            picture_url = sociallogin.account.get_avatar_url()

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(picture_url).read())
            img_temp.flush()
            author = Author()
            author.user = user
            author.profile_picture.save(
                f"{{author.user.username}}_profile", File(img_temp)
            )
            author.save()
        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name = sociallogin.account.extra_data['family_name']

            picture_url = sociallogin.account.extra_data['picture']
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(picture_url).read())
            img_temp.flush()
            author = Author()
            author.user = user
            author.name = user.username
            author.profile_picture.save(
                f"{{author.user.username}}_profile", File(img_temp)
            )
            author.save()
    print('ADDED')


@receiver(post_save)
def set_author_name(user=None, **kwargs):
    if user == None:
        user = User

    author = user.author
    author.name = user.username

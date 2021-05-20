from django import forms
from django.forms.widgets import Textarea
from tinymce import TinyMCE
from .models import Comment, Post, Comment, Author


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10, }
        )
    )
    overview = forms.CharField(
        widget=Textarea(
            attrs={'required': True, 'cols': 30, 'rows': 3}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content',
                  'thumbnail', 'categories')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content', )


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('profile_picture', )

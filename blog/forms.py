from django import forms

from .models import Post, Comment, About


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'postImg',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('aboutText', 'aboutImages')

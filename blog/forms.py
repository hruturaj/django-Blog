from django import forms
from .models import Post, Comment, Reply

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'message',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('message',)

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('message',)
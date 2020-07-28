from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

import misaka

# Create your models here.
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    image = models.ImageField(upload_to='blog_images', blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} => {}".format(self.title, self.user.username)

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    create_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def approve(self):
        self.approved_comments = True
        self.save()

    def __str__(self):
        return "{} : {}".format(self.post.title, self.author)

class Reply(models.Model):
    comment = models.ForeignKey('Comment', related_name='replies', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    message = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} : {}".format(self.comment.author, self.author)






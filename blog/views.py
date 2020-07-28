from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm, ReplyForm
from .models import Post, Comment, Reply
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

@login_required
def createPost(request):
    User = get_user_model()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            userSelected = User.objects.get(username=username)
            post = form.save(commit=False)
            post.user = userSelected
            post.save()
            return redirect('blog:postDetail', pk=Post.objects.latest('pk').pk)
    else:
        form = PostForm()
    return render(request, 'blog/createPost.html', {'form':form, 'formName':'Create'})

@login_required
def createComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.POST['username']
            comment.post = post
            comment.save()
            return redirect('blog:postDetail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/commentForm.html', {'form':form, 'formName':'Comment'})

def postList(request):
    data = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/postList.html', {'data':data})

def postDraft(request):
    data = Post.objects.filter(published_date__isnull=True).order_by('create_date')
    return render(request, 'blog/postDraft.html', {'data':data})

@login_required
def commentApprove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:postDetail', pk=comment.post.pk)

@login_required
def commentRemove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    postPK = comment.post.pk
    comment.delete()
    return redirect('blog:postDetail', pk=postPK)

def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/postDetail.html', {'post':post})

@login_required
def postEdit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.message = form.cleaned_data['message']
            post.image = form.cleaned_data['image']
            post.save()
            return redirect('blog:postDetail', pk=pk)
    else:
        form = PostForm(initial = {
            'title' : post.title, 'message' : post.message
        })
    return render(request, 'blog/createPost.html', {'form':form, 'formName':'Edit', 'postValue':post})

@login_required
def postDelete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:postList')

@login_required
def postPublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published()
    return redirect('blog:postDetail', pk=pk)

def userPosts(request, userName):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/userPosts.html', {'posts':posts, 'userPost':userName})

@login_required
def newReply(request, pk):
    commentObj = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = commentObj
            reply.author = request.POST['username']
            reply.save()
            return redirect('blog:postDetail', pk=commentObj.post.pk)
    else:
        form = ReplyForm()
    return render(request, 'blog/commentForm.html', {'form':form, 'formName':'Reply'})

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.postList, name='postList'),
    path('postDetail/<int:pk>', views.postDetail, name='postDetail'),
    path('postDraft/', views.postDraft, name='postDraft'),
    path('newPost/', views.createPost, name='newPost'),
    path('post/publish/<int:pk>', views.postPublish, name="postPublish"),
    path('post/edit/<int:pk>', views.postEdit, name='postEdit'),
    path('post/delete/<int:pk>', views.postDelete, name='postDelete'),
    path('newComment/<int:pk>', views.createComment, name='newComment'),
    path('comment/approve/<int:pk>', views.commentApprove, name='commentApprove'),
    path('comment/remove/<int:pk>', views.commentRemove, name="commentRemove"),
    path('userPosts/<str:userName>', views.userPosts, name="userPosts"),
    path('newReply/<int:pk>', views.newReply, name="newReply"),

]
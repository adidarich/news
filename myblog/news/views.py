from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, 'news/post/list.html', {'posts': posts})


def post_detail(request, id):  # детальная информация о посте
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, 'news/post/detail.html', {'post': post})

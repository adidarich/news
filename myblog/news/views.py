from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list,
                          2)  # создаем экземпляр класса Paginator с числом объектов, возвращаемых в расчете на страницу
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request, 'news/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):  # детальная информация о посте
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'news/post/detail.html', {'post': post})

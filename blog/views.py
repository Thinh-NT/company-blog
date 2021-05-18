from django.core import paginator
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from marketing.models import Signup


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'featured': featured,
        'latest': latest
    }
    return render(request, "blog/index.html", context)


def blog(request):
    most_recent = Post.objects.order_by('-timestamp')[:3]
    articles_list = Post.objects.all()
    paginator = Paginator(articles_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'most_recent': most_recent,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var
    }
    return render(request, "blog/blog.html", context)


def post(request, id):
    return render(request, "blog/post.html", {'id': id})

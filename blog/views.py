from django.contrib.auth import login
from django.db.models import Count, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Author, Category, Post
from .forms import CommentForm, PostForm, AuthorForm
from marketing.models import Signup


def get_category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))
    return queryset


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def index(request):
    featured = Post.objects.filter(featured=True).order_by('-timestamp')[:3]
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method == 'POST':
        email = request.POST['email']
        try:
            Signup.objects.get(email=email)
            messages.info(request, "You're already subcribed, thanks though.")
            return redirect('index')
        except Signup.DoesNotExist:
            new_signup = Signup()
            new_signup.email = email
            new_signup.save()
            messages.success(
                request, "Thank you for your subscription, now you'll be charge 15$ a month...")
            return redirect('index')
    context = {
        'featured': featured,
        'latest': latest
    }
    return render(request, "blog/index.html", context)


def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    articles_list = Post.objects.all().order_by('-timestamp')
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
        'page_request_var': page_request_var,
        'category_count': category_count,
    }
    return render(request, "blog/blog.html", context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    title = post.title
    post.views_count += 1
    post.save()
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('detail-post', kwargs={
                'id': post.id
            }))
    context = {
        'post': post,
        'category_count': category_count,
        'most_recent': most_recent,
        'form': form,
        'title': title
    }
    return render(request, "blog/post.html", context)


@login_required
def create_post(request):
    title = 'create post'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("detail-post", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form': form,
        'title': title
    }
    return render(request, "blog/create_post.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        p_form = AuthorForm(
            request.POST, request.FILES, instance=request.user.author
        )
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f"You account has been updated")
            return redirect("profile")

    else:
        p_form = AuthorForm(instance=request.user.author)

    author = request.user.author
    posts = Post.objects.all().filter(author=request.user.author)[:3]
    category_count = posts.values(
        'categories__title').annotate(Count('categories__title'))
    context = {
        "author": author,
        "p_form": p_form,
        "category_count": category_count,
        "posts": posts,
        "title": "profile"
    }
    return render(request, "blog/profile.html", context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset,
        'title': 'search'
    }
    return render(request, 'blog/search_result.html', context)


def category_posts_view(request, category):
    category = Category.objects.get(title=category)
    queryset = category.post.all()
    title = category
    context = {
        'queryset': queryset,
        'title': title
    }
    return render(request, 'blog/category_posts.html', context)


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/create_post.html", context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.info(request, "Your post have been deleted.")
    return redirect(reverse("blog"))


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("detail-post", kwargs={
            'id': form.instance.id
        }))


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'blog/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = get_category_count()
        context['most_recent'] = Post.objects.order_by('-timestamp')[:3]
        context['title'] = 'Delete'
        return context

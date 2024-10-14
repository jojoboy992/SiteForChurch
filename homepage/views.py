from django.shortcuts import *
from django.http import *
from django.views.generic import *
from .models import *
from .forms import PostForm


# Create your views here.

class HomePage(TemplateView):
    template_name = 'index.html'


class AboutPage(TemplateView):
    template_name = 'about.html' 

class ContactPage(TemplateView):
    template_name = 'contact.html'        

# Custom 404 view (already correct)
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def post_list(request):
    posts = Post.objects.all().order_by('-created_at') 
    return render(request, 'events-activities.html', {'posts': posts})

# Post detail view (accessible to all users)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

# Restrict to admin users only
def post_new(request):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})

# Restrict to admin users only
def post_edit(request, pk):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

# Restrict to admin users only
def post_delete(request, pk):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog')

# Restrict to admin users only
def post_confirm_delete(request, pk):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog')
    return render(request, 'confirm_delete.html', {'post': post})
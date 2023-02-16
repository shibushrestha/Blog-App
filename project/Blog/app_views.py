from django.shortcuts import (render, redirect, get_object_or_404, get_list_or_404)
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import CreateBlogPostForm

# The home view
def home(request):
    all_post = get_list_or_404(Post)
    context = {
        'all_post': all_post
    }
    return render(request, 'Blog/home.html', context)

# Post Detail view
def post_detail(request, post_slug):
 
    post = get_object_or_404(Post, slug=post_slug)
    context = {
        'post': post,
    }
    return render(request, 'Blog/detail.html', context)

# Create post view
@login_required
def create_post(request, user_username):
   
    form = CreateBlogPostForm()
    if request.method == "POST":
        form = CreateBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            cover_images = form.cleaned_data.get('cover_images')
            
            post = Post.objects.create(user=user, title=title, body=body, cover_images=cover_images)
            # For now lets create the redirect url like this
            return redirect('/Blog/post_detail/' + post.slug + "/")

    return render(request, 'Blog/create.html', {'form':form,})

# Delete Post view

def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.method == "POST":
        if post.user == request.user:
            post.delete()
            return redirect('Blog:home')
    else:
        return redirect(post.user.userprofile)

from django.shortcuts import (render, redirect, get_object_or_404, get_list_or_404)
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Blog, UserProfile
from .forms import(UserRegisterForm, UserAuthenticationForm, CreateBlogForm, UpdateProfileForm)

def home(request):
    all_blog = get_list_or_404(Blog)
    context = {
        'all_blog': all_blog
    }
    return render(request, 'Blog/home.html', context)

def register_user(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = User(username=username)
            user.set_password(password)
            user.save()
            return redirect('home')
    return render(request, 'Blog/register-user.html', context={'form':form})

def user_login(request):
    form = UserAuthenticationForm()
    if request.method == "POST":
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # When you use login_required decorator the 'next' value is used to take the user to
            # the next page after uccessful login, if there is no 'next' value, LOGIN_REDIRECT_URL is used 
            # To get the value of 'next' do this, you can get the value of next in the template like so request.GET('next')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    return render(request, 'Blog/user-login.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def update_user_profile(request):
    user = request.user
    userprofile, created = UserProfile.objects.get_or_create(user=user)

    form = UpdateProfileForm(instance=userprofile)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            profile_image = form.cleaned_data.get('profile_image')
            youtube_account = form.cleaned_data.get('youtube_account')
            instagram_account = form.cleaned_data.get('instagram_account')
            update_userprofile = UserProfile.objects.filter(user=user).update(
                description = description,
                profile_image = profile_image,
                youtube_account = youtube_account,
                instagram_account = instagram_account
            )

            # for now lets redirect to home
            return redirect('home')
    return render(request, 'Blog/update_profile.html', {'form':form})


@login_required
def user_profile(request, user_username):
    user = get_object_or_404(User, username = user_username)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_all_blog = user.blog_set.all()
    context ={
        'user':user, 
        'user_profile':user_profile,
        'user_all_blog':user_all_blog,
        }
    return render(request, 'Blog/userprofile.html', context)

@login_required
def create_blog(request):
    form = CreateBlogForm()
    if request.method == "POST":
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            cover_images = form.cleaned_data.get('cover_images')
            
            blog = Blog.objects.create(user=user, title=title, body=body, cover_images=cover_images)
            
            #return redirect('')

    return render(request, 'Blog/create.html', {'form':form})


def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    context = {
        'blog':blog,
    }
    return render(request, 'Blog/detail.html', context)

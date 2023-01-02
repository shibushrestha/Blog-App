from django.shortcuts import (render, redirect, get_object_or_404, get_list_or_404)
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Post, UserProfile
from .forms import(UserRegisterForm, UserAuthenticationForm, CreateBlogPostForm, UpdateProfileForm)

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
def create_post(request):
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
# Anyone can delete any post, even if a user is not logged_in or anonymous, or even if its not theirs post
# This is not certainly what we want
# Need to achieve a functionality where only the user logged can delete the post and only if its theirs post
@login_required
@require_http_methods(['POST'])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.user == request.user:
        post.delete()
        return redirect('Blog:home')
    else:
        return HttpResponse("<h1>You don't have permission to delete this post.</h1>")





#########################################################################################
    #######  ALL THE VIEWS RELATED TO USER AUTHENTICATION AND USER PROFILE  #########
#########################################################################################




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
            return redirect('Blog:login')
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
            return redirect('Blog:home')
    return render(request, 'Blog/user-login.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('Blog:home')


# User profile view
def user_profile(request, user_username):
    try:
        user = User.objects.get(username=user_username)
    except ObjectDoesNotExist:
        return HttpResponse('<h1>User doesnot exist</h1>')
    if user == request.user:
        user_profile = get_object_or_404(UserProfile, user=user)
        user_all_post = user.post_set.all()
        context ={
            'user':user, 
            'user_profile':user_profile,
            'user_all_post':user_all_post,
        }
        return render(request, 'Blog/userprofile.html', context)
    elif user != request.user and User.objects.filter(username=user.username).exists():
        return redirect('Blog:login')

# User profile update view
def update_user_profile(request, user_username):
    user = User.objects.get(username=user_username)
    if user == request.user:
        userprofile = get_object_or_404(UserProfile, user=user)
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
                return redirect(userprofile)

        return render(request, 'Blog/update_profile.html', {'form':form})
    else:
        return redirect("Blog:login")
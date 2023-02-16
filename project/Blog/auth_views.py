from django.shortcuts import (render, redirect, get_object_or_404, get_list_or_404)
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from Blog.models import UserProfile
from django.forms import UserRegisterForm, UserAuthenticationForm, UpdateProfileForm


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
        raise Http404
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
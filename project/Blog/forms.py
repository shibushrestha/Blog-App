from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from tinymce.widgets import TinyMCE
from .models import Post, UserProfile


class CreateBlogPostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'body', 'cover_images')
        widgets = {
            'title':forms.TextInput(attrs={
            'placeholder':'Your post title here...', 'size':'50', 'class':'post-title no-outline'}),
            'body': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
        

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder':'Username', 'size':'30', 'class':'form-control form-control-sm', 'autofocus':False}
        )
        self.fields['password1'].widget.attrs.update(
            {'placeholder':'Enter a strong password', 'size':'30', 'class':'form-control form-control-sm'}
        )
        self.fields['password2'].widget.attrs.update(
            {'placeholder':'Confirm password', 'size':'30', 'class':'form-control form-control-sm'}
        )


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder':'Username', 'size':'30', 'class':'form-control form-control-sm', 'autofocus':False}
        )
        self.fields['password'].widget.attrs.update(
            {'placeholder':'Enter password', 'size':'30', 'class':'form-control form-control-sm'}
        )


class UpdateProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('description', 'profile_image', 'youtube_account', 'instagram_account')
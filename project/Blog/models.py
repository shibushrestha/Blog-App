from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Blog(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    body = RichTextField()
    cover_images = models.ImageField(blank=True, null=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(max_length=1000, blank=True)
    likes = models.PositiveSmallIntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    
    class Meta():
        
        ordering = ['-created_date_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def get_cover_image_url(self):
        if self.cover_images and hasattr(self.cover_images, 'url'):
            return self.cover_images.url
        else:
            return "/static/Blog/images/default_blog_cover_image.webp"


class UserProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    youtube_account = models.URLField(blank=True, null=True)
    instagram_account = models.URLField(blank=True, null=True)
    follower = models.ManyToManyField(to=get_user_model(),  related_name="user_follower", blank=True)
    following = models.ManyToManyField(to=get_user_model(), related_name="user_following", blank=True)

    def __str__(self):
        return self.user.username + ' Profile'

    @property
    def get_profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return "/static/Blog/images/default_profile_image.webp"


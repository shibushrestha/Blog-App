from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    body = RichTextField()
    cover_images = models.ImageField(blank=True, null=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
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
        
    def get_absolute_url(self):
        return reverse("Blog:detail", kwargs={"post_slug": self.slug})


# Discuss model
# User can discuss about post
class PostDiscussion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ManyToManyField(to=get_user_model())
    body = RichTextField()
    discuss_date = models.DateTimeField(auto_now_add=True)


# User Profile 
class UserProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    youtube_account = models.URLField(blank=True, null=True)
    instagram_account = models.URLField(blank=True, null=True)
    # User followers and following needs a logic
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
    
    def get_absolute_url(self):
        return reverse("Blog:profile", kwargs={"user_username": self.user.username})
    

# A receiver function that listens to post_save signal and creates user profile when new user get registered 
@receiver(post_save, sender=User)
def user_profile_handler(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# lets make a madel "Drafts" where user can save their post before publishing it to the Blog model where it acttually 
# gets displayed for all the user
class DraftPost(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE,)
    title = models.CharField(max_length=1000)
    body = RichTextField()
    cover_images = models.ImageField(blank=True, null=True, upload_to="draft_images")
    created_date_time = models.DateTimeField(auto_now_add=True)


    class Meta():
        ordering = ['-created_date_time']

    def __str__(self):
        return self.title

    @property
    def get_cover_image_url(self):
        if self.cover_images and hasattr(self.cover_images, 'url'):
            return self.cover_images.url
        else:
            return "/static/Blog/images/default_blog_cover_image.webp"
        
    def get_absolute_url(self):
        return reverse("Blog:draft_post_detail", kwargs={"draftpost_slug": self.slug})
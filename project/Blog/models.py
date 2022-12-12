from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField



class Blog(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    body = RichTextField()
    blog_images = models.ImageField(blank=True, null=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(max_length=1000, blank=True)
    likes = models.PositiveSmallIntegerField(blank=True, null=True)
    
    class Meta():
        
        ordering = ['-created_date_time']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    youtube_account = models.URLField(blank=True, null=True)
    instagram_account = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username + ' Profile'

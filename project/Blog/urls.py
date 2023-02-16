from django.urls import path, re_path

from Blog import views
from Blog import auth_views

app_name = "Blog"
urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'^post_detail/(?P<post_slug>[a-zA-Z0-9-]+)/?$', views.post_detail, name='detail'),

    re_path(r'^register/$', auth_views.register_user, name="register"),
    re_path(r'^login/$', auth_views.user_login, name="login"),
    re_path(r'^logout/$', auth_views.user_logout, name="logout"),
    re_path(r'^(?P<user_username>[a-zA-Z0-9]+)/?$', auth_views.user_profile, name="profile"),
    re_path(r'^(?P<user_username>[a-zA-Z0-9]+)/profileupdate/', auth_views.update_user_profile, name="updateprofile"),

    re_path(r'^create/$', views.create_post, name="create"),
    re_path(r'^(?P<post_id>[\d]+)/?delete/$', views.delete_post, name="delete_post"),

    
]

from django.urls import path, re_path

from . import views


app_name = "Blog"
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_user, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('create/', views.create_post, name="create"),
    path('post_detail/<slug:post_slug>/', views.post_detail, name='detail'),
    path('<int:post_id>/delete/', views.delete_post, name="delete_post"),
    path('<str:user_username>/', views.user_profile, name="profile"),
    path('<str:user_username>/profileupdate/', views.update_user_profile, name="updateprofile")
    
]

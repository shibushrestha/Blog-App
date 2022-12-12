from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_user, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('create/', views.create_blog, name="create"),
    path('detail/<int:blog_id>/', views.blog_detail, name='detail'),
    path('profileupdate/', views.update_user_profile, name="updateprofile"),
    path('<str:user_username>/', views.user_profile, name="profile")
    
]

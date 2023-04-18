from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),#home page
    path('signup', views.sign_up, name='sign_up'),#register form
    path('create-post', views.create_post, name='create_post'),#create post form
    path('password_reset', views.password_reset_request, name='password_reset'),
    path('my_profile/', views.my_profile, name='my_profile'), #display account owner's profile
    path('edit_my_profile/', views.edit_my_profile, name='edit_my_profile'),#edit/update profile by an account owner
    path('members/', views.members, name='members'),#display all the users in list
    path('members/details/<int:id>', views.details, name='details'),#display all the user in details
]
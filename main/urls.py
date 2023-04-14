from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signup', views.sign_up, name='sign_up'),
    path('password_reset', views.password_reset_request, name='password_reset'),
]
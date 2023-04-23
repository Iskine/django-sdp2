from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),#home page
    path('signup', views.sign_up, name='sign_up'),#register form
    path('create-post', views.create_post, name='create_post'),#create post form
    path('my_profile/', views.my_profile, name='my_profile'), #display account owner's profile
    path('edit_my_profile/', views.edit_my_profile, name='edit_my_profile'),#edit/update profile by an account owner
    path('members/', views.members, name='members'),#display all the users in list
    path('members/details/<int:id>', views.details, name='details'),#display all the user in details
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),#display all the user in details
    path('edit_user/<int:id>', views.edit_user, name='edit_user'), #for admin to edit user account
    path('delete_my_account/<int:id>', views.delete_my_account, name='delete_my_account'), #delete my own account
    path('change_user_password/<int:id>', views.change_user_password, name='change_user_password'), #for the admin to change the user password
    path('project_list/', views.project_list, name='project_list'),#list all of the project 
    path('create_project', views.create_project, name='create_project'),# create new project form
    path('delete_project/<int:id>', views.delete_project, name='delete_project'),#delete a project 
    path('project/<int:project_id>/tasks', views.task_list, name='task_list'),#list of task
    path('project/<int:project_id>/tasks/create_task', views.create_task, name='create_task'),#create new task form
    path('project/<int:project_id>/tasks/<int:task_id>/update_task', views.update_task, name='update_task'),#edit/update a task
    path('project/<int:project_id>/tasks/<int:task_id>/delete_task', views.delete_task, name='delete_task'),#delete a task
    path('get-tasks/<int:project_id>/', views.get_tasks, name='get_tasks'),

]
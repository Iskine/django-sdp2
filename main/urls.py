from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),#home page
    path('login/', views.login_view, name='login'),
    path('signup/', views.sign_up, name='sign_up'),#register form
    path('my_profile/', views.my_profile, name='my_profile'), #display account owner's profile
    path('update_my_profile/', views.update_my_profile, name='update_my_profile'),#update profile by an account owner
    path('members/', views.members, name='members'),#display all the users in list
    path('members/details/<int:id>', views.details, name='details'),#display all the user in details
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),#display all the user in details
    path('update_user/<int:id>', views.update_user, name='update_user'), #for admin to update user account
    path('delete_my_account/<int:id>', views.delete_my_account, name='delete_my_account'), #delete my own account
    path('change_user_password/<int:id>', views.change_user_password, name='change_user_password'), #for the admin to change the user password
    path('project_list/', views.project_list, name='project_list'),#list all of the project 
    path('project_details/<int:project_id>', views.project_details, name='project_details'),#Detail of the project 
    path('create_project', views.create_project, name='create_project'),# create new project form
    path('project/<int:project_id>/update_project/', views.update_project, name='update_project'),# update a project 
    path('delete_project/<int:project_id>', views.delete_project, name='delete_project'),#delete a project 
    path('project/<int:project_id>/tasks', views.task_list, name='task_list'),#list of task
    path('project/<int:project_id>/tasks/<int:task_id>/', views.task_details, name='task_details'),#task details
    path('project/<int:project_id>/tasks/create_task', views.create_task, name='create_task'),#create new task form
    path('project/<int:project_id>/tasks/<int:task_id>/update_task', views.update_task, name='update_task'),#update a task
    path('project/<int:project_id>/tasks/<int:task_id>/delete_task', views.delete_task, name='delete_task'),#delete a task
    path('get-tasks/<int:project_id>/', views.get_tasks, name='get_tasks'),#views for getting task to display in the gantt chart
    path('create_team/', views.create_team, name='create_team'),
    path('team_list/', views.team_list, name='team_list'),
    path('team/<int:pk>/delete/', views.delete_team, name='delete_team'),
    path('team/<int:pk>/update/', views.update_team, name='update_team'),
    path('tasks/<int:task_id>/create_sub_task/', views.create_sub_task, name='create_sub_task'),
    path('project/<int:project_id>/tasks/<int:task_id>/sub_task_list/', views.sub_task_list, name='sub_task_list'),
    path('project/<int:project_id>/tasks/<int:task_id>/subtasks/<int:sub_task_id>/update/', views.update_sub_task, name='update_sub_task'),
    path('project/<int:project_id>/tasks/<int:task_id>/subtasks/<int:sub_task_id>/delete/', views.delete_sub_task, name='delete_sub_task'),
]
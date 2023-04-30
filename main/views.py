from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProjectForm, TaskForm, TeamForm, MembershipForm, SubTaskForm, CustomMyProfileUpdateForm, CustomUserForm ,CustomUserPasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from .models import Project, Task, Team, Membership, SubTask
from django.contrib.auth.models import User, Group
from django.template import loader 
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.contrib import messages 
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.db.models import Sum
from django.urls import reverse


#home page
def home(request): 
    return render(request, 'frontend/index.html', {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.') # add error to form
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})



#register form

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your registration was successful. Welcome!')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'frontend/signup.html', {"form": form})


#display the account owner's profile
@login_required(login_url="/login")
def my_profile(request):
    user = User.objects.all().values()
    template = loader.get_template('frontend/myprofile.html')
    context = {
        'user': user, 
    }
    return HttpResponse(template.render(context, request))


#the account owner can update their profile information
@login_required(login_url="/login")
def update_my_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = CustomMyProfileUpdateForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            return redirect('my_profile')
        return render(request, "frontend/updatemyprofile.html", {'form': form})
    else:
        messages.success(request, ("You must be logged in to update your profile"))
        return redirect('/login')
    


# Delete my profile
@login_required(login_url="/login")
def delete_my_account(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        logout(request)
        return redirect('login')
    else: context = {
            'user': user,
    }
    return render(request, 'frontend/deletemyprofile.html', context)
    



# Delete user profile by admin
@login_required(login_url="/login")
@user_passes_test(lambda user: user.is_superuser)
def delete_user(request, id):
    account_to_delete = User.objects.get(id=id)
    if request.method == 'POST':
        account_to_delete.delete()
        return redirect('members')
    else:
        context = {
            'memberdetails' : account_to_delete,
        }
    return render(request, 'frontend/deleteuser.html', context)



# update user without password by admin
@user_passes_test(lambda user: user.is_superuser)
def update_user(request, id):
    now_user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserForm(request.POST, instance=now_user)
        if form.errors:
           print(form.errors)

        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()  # Add this line to save the ManyToMany relationship (groups)
            return redirect('members')
        
    else:
        form = CustomUserForm(instance=now_user)
        form.fields['is_superuser'].initial = now_user.is_superuser
        form.fields['is_staff'].initial = now_user.is_staff
        form.fields['is_active'].initial = now_user.is_active
        form.fields['groups'].initial = now_user.groups.all()

    context = {
        'form': form,
        'now_user': now_user, 
    }
    return render(request, 'frontend/updateuser.html', context)



#update user password by admin
@login_required(login_url="/login")
@user_passes_test(lambda user: user.is_superuser)
def change_user_password(request, id):
    now_user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = CustomUserPasswordChangeForm(request.POST, instance=now_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User password has been updated.')
            return redirect('members')
    else:
        form = CustomUserPasswordChangeForm(instance=now_user)

    context = {
        'form': form,
    }
    return render(request, 'frontend/updateuserpassword.html', context)





#display all of the user 
@login_required(login_url="/login")
def members(request):
  mymembers = User.objects.all()
  template = loader.get_template('frontend/userlist.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))



#display the user in details
@login_required(login_url="/login")
def details(request, id):
  memberdetails = User.objects.get(id=id)
  template = loader.get_template('frontend/userdetails.html')
  context = {
    'memberdetails': memberdetails,
  }
  return HttpResponse(template.render(context, request))




# list member team
def team_list(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        my_teams = teams
        can_create_team = False
        can_update_team = False
        
    elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        my_teams = teams
        can_create_team = False
        can_update_team = False
        
    elif user.groups.filter(name='team_manager').exists():
        teams = Team.objects.all()
        my_teams = teams
        can_create_team = True
        can_update_team = True
    else:
        teams = Team.objects.all()
        my_teams = []
        can_create_team = False
        can_update_team = False
    return render(request, 'frontend/teamlist.html', {'teams': teams, 'my_teams': my_teams, 'can_create_team':can_create_team, 'can_update_team':can_update_team})





#create team
@login_required(login_url="/login")
def create_team(request):
    if not request.user.groups.filter(name='team_manager').exists():
        raise PermissionDenied

    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        membership_form = MembershipForm(request.POST)
        if team_form.is_valid() and membership_form.is_valid():
            team = team_form.save()
            membership_form.save(team=team)
            return redirect('team_list')
    else:
        team_form = TeamForm()
        membership_form = MembershipForm()

    teams = Team.objects.all()
    memberships = Membership.objects.all()
    team_managers = Group.objects.get(name='team_manager').user_set.all()

    return render(request, 'frontend/createteam.html', {'team_form': team_form, 'membership_form': membership_form, 'teams': teams, 'memberships': memberships, ' team_managers':  team_managers})




#update team
def update_team(request, pk):
    if not request.user.groups.filter(name='team_manager').exists():
        raise PermissionDenied
     
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team_form = TeamForm(request.POST, instance=team)
        membership_form = MembershipForm(request.POST)
        if team_form.is_valid() and membership_form.is_valid():
            team = team_form.save()
            # Update the membership by removing the existing ones and adding the selected ones
            team.membership_set.all().delete()
            membership_form.save(team=team)
            return redirect('team_list')
    else:
        team_form = TeamForm(instance=team, initial={
            'team_leader': team.team_leader.id if team.team_leader else None, 
            'team_manager': team.team_manager.id if team.team_manager else None, 
        })
        membership_form = MembershipForm(initial={
            'members': [user.id for user in team.members.all()],
            })
    return render(request, 'frontend/updateteam.html', {'team_form': team_form, 'membership_form': membership_form, 'team': team})






# delete team
def delete_team(request, pk):
    if not request.user.groups.filter(name='team_manager').exists():
        raise PermissionDenied
    
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'frontend/deleteteam.html', {'team': team, 'pk': pk})




#create new project
@login_required
def create_project(request):
    user = request.user
    if user.groups.filter(name='team_member').exists() or user.groups.filter(name='team_leader').exists():
      
        if request.method == 'POST':
            form = ProjectForm(request.user, request.POST)
            if form.is_valid():
                project = form.save(commit=False)
                project.created_by = request.user
                project.save()
                return redirect('project_list')
        else:
            form = ProjectForm(request.user)
        return render(request, 'frontend/createproject.html', {'form': form})
    else: 
         raise PermissionDenied







#display list of projects
@login_required(login_url="/login")
def project_list(request):
  user = request.user
  if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        projects = Project.objects.filter(Q(team__in=teams) | Q(created_by=user))
        can_create_project = True
  elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        projects = Project.objects.filter(Q(team__in=teams) | Q(created_by=user))
        can_create_project = True
  elif user.groups.filter(name='team_manager').exists():
        teams = Team.objects.all()
        projects = Project.objects.filter(team__in=teams)
        can_create_project = False
  else:
        projects = Project.objects.filter(created_by=user)
        can_create_project = False
  return render(request, 'frontend/projectlist.html', {'projects':projects, 'can_create_project': can_create_project}) 







# project details
def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Get the team for the project if it exists
    team = project.team
    if team:
        # Get the members of the team
        members = team.members.all()
    else:
        members = []
    # Check if the current user is a team leader
    is_team_leader = request.user.groups.filter(name='team_leader').exists()
    # Check if the current user is a team member
    is_team_member = request.user.groups.filter(name='team_member').exists()
    return render(request, 'frontend/projectdetails.html', {'project': project, 'team': team, 'members': members, 'is_team_leader': is_team_leader, 'is_team_member':is_team_member})



# Update Project
def update_project(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if not user.groups.filter(Q(name='team_leader') | Q(name='team_member')).exists() and user != project.created_by:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, user=user)
        if form.is_valid():
            form.save()
            return redirect('project_details', pk=project.pk)
    else:
        form = ProjectForm(instance=project, user=user)
    return render(request, 'main/update_project.html', {'form': form, 'project': project})

# Delete project
@login_required(login_url="/login")
def delete_project(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if not user.groups.filter(name='team_leader').exists():
        raise PermissionDenied

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(request, 'main/delete_project.html', {'project': project})




# Create project task
@login_required(login_url='/login')
def create_task(request, project_id):
    project = Project.objects.get(id=project_id)

    if not (request.user.groups.filter(name='team_member').exists() or request.user.groups.filter(name='team_leader').exists()):
         raise PermissionDenied
         
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm()
    return render(request, 'main/create_task.html', {'form': form, 'project': project})





# list the task in each project
@login_required(login_url="/login")
def task_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = project.tasks.all()
    is_team_member = request.user.groups.filter(name='team_member').exists()
    is_team_leader = request.user.groups.filter(name='team_leader').exists()
    return render(request, 'frontend/tasklist.html', {'project': project, 'tasks': tasks, 'is_team_member': is_team_member, 'is_team_leader': is_team_leader})



# update task
@login_required(login_url="/login")
def update_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    project = task.project

    if not (request.user.groups.filter(name='team_member').exists() or request.user.groups.filter(name='team_leader').exists()):
        raise PermissionDenied

    # Allow all users in the project to update task
    elif project and (user == project.created_by or (project.team and user in project.team.members.all()) or Membership.objects.filter(team=project.team, user=user).exists()):
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('task_list', project_id=project_id)
        else:
            form = TaskForm(instance=task)
        is_team_member = request.user.groups.filter(name='team_member').exists()
        is_team_leader = request.user.groups.filter(name='team_leader').exists()
        return render(request, 'main/update_task.html', {'task':task, 'form': form, 'project_id': project_id, 'task_id': task_id, 'is_team_member': is_team_member, 'is_team_leader': is_team_leader})
    else:
        return HttpResponseForbidden()




# delete task
@login_required(login_url="/login")
def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user

    # Check if the current user is a team leader
    is_team_leader = user.groups.filter(name='team_leader').exists()

    # Only allow team leaders to delete tasks
    if not is_team_leader:
        raise PermissionDenied

    if request.method == 'POST':
        task.delete()
        return redirect('task_list', project_id=project_id)

    return render(request, 'main/delete_task.html', {'task':task, 'project_id': project_id, 'task_id': task_id, 'is_team_leader': is_team_leader})



# # get task data for gantt chart
# from django.http import JsonResponse

# def get_tasks(request, project_id):
#     # get_object_or_404() function to retrieve the project object with the given ID. If the object doesn't exist, it raises a Http404 exception.
#     project = get_object_or_404(Project, pk=project_id)
#     # filter() method of the Task model to retrieve all the tasks that belong to the project. 
# 	# set the project in Project to equal to project in the Task
# 	# The values() method is used to specify which fields of the Task model should be included in the queryset.
#     tasks = Task.objects.filter(project=project).values('id','title', 'start_date', 'end_date')
#     # creates an empty list data to store the JSON data for each task.
#     data = []
#     # iterates over each task in the queryset 
#     for task in tasks:
# 	# and calculates the duration of the task by subtracting the start date from the end date and adding 1 (since the start and end dates are inclusive).
#         start_date = task['start_date']
#         end_date = task['end_date']
#         duration = (end_date - start_date).days + 1
    
#         data.append({
#             'Task_ID': task['title'],
#             'Task_Name': task['title'],
#             'Start_Date': start_date.strftime('%Y-%m-%d'),
#             'End_Date': end_date.strftime('%Y-%m-%d'),
#             'Duration': duration,
#             'Percent_Complete': 30,
#             'Dependencies': None
#         })
#     return JsonResponse(data, safe=False)


from django.http import JsonResponse
from django.db.models import Count

def get_tasks(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project=project).values('id','title', 'start_date', 'end_date')
    data = []
    for task in tasks:
        start_date = task['start_date']
        end_date = task['end_date']
        duration = (end_date - start_date).days + 1
        
        # Calculate total and completed subtasks for the task
        subtasks = SubTask.objects.filter(task__id=task['id']).aggregate(total_count=Count('id'), completed_count=Count('id', filter=Q(completed=True)))
        total_subtasks = subtasks['total_count'] or 1 # avoid divide by zero error
        completed_subtasks = subtasks['completed_count'] or 0
        
        # Calculate percentage completion
        percent_complete = round((completed_subtasks / total_subtasks) * 100)
        
        data.append({
            'Task_ID': task['title'],
            'Task_Name': task['title'],
            'Start_Date': start_date.strftime('%Y-%m-%d'),
            'End_Date': end_date.strftime('%Y-%m-%d'),
            'Duration': duration,
            'Percent_Complete': percent_complete,
            'Dependencies': None
        })
        
    return JsonResponse(data, safe=False)








from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import SubTask, Task
from .forms import SubTaskForm

def create_sub_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project
    user = request.user

    if not (user == project.created_by or (project.team and user in project.team.members.all()) or Membership.objects.filter(team=project.team, user=user).exists()):
        return HttpResponseForbidden("You don't have permission to create subtasks in this task.")

    if request.method == "POST":
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.created_by = request.user
            subtask.task = task
            subtask.save()
            return redirect("sub_task_list", project_id=project.id, task_id=task.id)  # Assuming you have a sub_task_list view
    else:
        form = SubTaskForm()

    context = {
        "task_id": task_id,
        "project_id": project.id,
        "form": form,
        "task": task,
    }

    return render(request, 'main/create_sub_task.html', context)



@login_required(login_url="/login")
def sub_task_list(request, project_id, task_id):

    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, project=project)
 
    if not (request.user.groups.filter(name='team_member').exists() or request.user.groups.filter(name='team_leader').exists()):
        raise PermissionDenied


    sub_tasks = SubTask.objects.filter(task=task)

    return render(request, 'main/sub_task_list.html', {'sub_tasks': sub_tasks, 'project_id': project_id, 'task_id': task_id, 'project': project, 'task': task})



@login_required
def update_sub_task(request, project_id, task_id, sub_task_id):
    sub_task = get_object_or_404(SubTask, pk=sub_task_id)
    task = sub_task.task
    project = get_object_or_404(Project, pk=project_id)

    # Check user permissions
    if not (request.user.groups.filter(name='team_member').exists()):
        raise PermissionDenied

    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=sub_task)
        if form.is_valid():
            form.save()
            return redirect('sub_task_list', project_id=project.id, task_id=task.id)
    else:
        form = SubTaskForm(instance=sub_task)

    context = {
        'form': form,
        'sub_task_id': sub_task_id,
        'project_id': project_id,
        'task_id': task_id,
        'sub_task': sub_task,
    }

    return render(request, 'main/update_sub_task.html', context)





@login_required
def delete_sub_task(request, sub_task_id, project_id, task_id):
    sub_task = get_object_or_404(SubTask, pk=sub_task_id)
    task = sub_task.task
    project = task.project

    # Check user permissions
    if not (request.user == project.created_by or (project.team and request.user in project.team.members.all()) or Membership.objects.filter(team=project.team, user=request.user).exists()):
        return HttpResponseForbidden("You don't have permission to delete subtasks in this project.")

    if request.method == 'POST':
        sub_task.delete()
        return redirect('sub_task_list', project_id=project.id, task_id=task.id)

    context = {
        'sub_task_id': sub_task_id,
        'project_id': project_id,
        'task_id': task_id,
        'sub_task': sub_task,
    }

    return render(request, 'main/delete_sub_task.html', context)






@login_required(login_url="/login")
def test123(request):
  user = request.user
  if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        projects = Project.objects.filter(Q(team__in=teams) | Q(created_by=user))
        can_create_project = True
  elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        projects = Project.objects.filter(Q(team__in=teams) | Q(created_by=user))
        can_create_project = True
  elif user.groups.filter(name='team_manager').exists():
        teams = Team.objects.all()
        projects = Project.objects.filter(team__in=teams)
        can_create_project = False
  else:
        projects = Project.objects.filter(created_by=user)
        can_create_project = False
  return render(request, 'main/project_list.html', {'projects':projects, 'can_create_project': can_create_project}) 






















from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProjectForm, TaskForm, TeamForm, MembershipForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login, logout
from .models import Project, Task, Team, Membership
from django.contrib.auth.models import User, Group
from django.template import loader 
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages 
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied









#home page
@login_required(login_url="/login")#if not login, redirect to /login
def home(request): 
	return render(request, 'main/home.html', {})


#register form
def sign_up(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/home') 
	else: 
		form = RegisterForm()

	return render(request, 'registration/sign_up.html', {"form": form}) 


#display the account owner's profile
@login_required(login_url="/login")
def my_profile(request):
	pf = User.objects.all().values()
	template = loader.get_template('main/my_profile.html')
	context = {
		'pf': pf, 
	}
	return HttpResponse(template.render(context, request))

#the account owner can update their profile information
@login_required(login_url="/login")
def update_my_profile(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		form = RegisterForm(request.POST or None, instance=current_user)
		if form.is_valid():
			form.save()
			login(request, current_user)
			messages.success(request, ("Your Profile has been updated"))
			return redirect('my_profile')
		
		return render(request, "main/update_my_profile.html", {'form':form})
	else:
		messages.success(request, ("You must logged in to update profile"))
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
	return render(request, 'main/delete_my_account.html', context)
	

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
	return render(request, 'main/delete_user.html', context)

# Update user profile by admin(without password)
@login_required(login_url="/login")
@user_passes_test(lambda user: user.is_superuser)
def update_user(request, id):
	now_user = get_object_or_404(User, id=id)
	if request.method == 'POST':
		form = UserChangeForm(request.POST, instance=now_user)
		form.fields['password'].required = False
		form.fields['last_login'].required = False
		form.fields['is_superuser'].required = False
		form.fields['groups'].required = False
		form.fields['date_joined'].required = False
		form.fields['user_permissions'].required = False
			
		if form.is_valid():
			form.save()
			messages.success(request, 'User profile has been updated.')
			return redirect('members')
		
	else:
		form = UserChangeForm(instance=now_user)
		form.fields.pop('password')
		form.fields.pop('last_login')
		# form.fields.pop('is_superuser')
		# form.fields.pop('groups')
		form.fields.pop('date_joined')
		form.fields.pop('user_permissions')

	context = {
		'form': form,
	}
	return render(request, 'main/update_user.html', context)

#update user password by admin
@login_required(login_url="/login")
@user_passes_test(lambda user: user.is_superuser)
def change_user_password(request, id):
	now_user = get_object_or_404(User, id=id)
	if request.method == 'POST':
		form = RegisterForm(request.POST, instance=now_user)
		if form.is_valid():
			form.save()
			messages.success(request, 'User profile has been updated.')
			return redirect('members')
	else: 
		form = RegisterForm(instance=now_user)
	context = {
		'form': form, 
	}
	return render(request, 'main/change_user_password.html', context)

#display all of the user 
@login_required(login_url="/login")
def members(request):
  mymembers = User.objects.all().values()
  template = loader.get_template('main/all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

#display the user in details
@login_required(login_url="/login")
def details(request, id):
  memberdetails = User.objects.get(id=id)
  template = loader.get_template('main/members_details.html')
  context = {
    'memberdetails': memberdetails,
  }
  return HttpResponse(template.render(context, request))


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
                return redirect('home')
        else:
            form = ProjectForm(request.user)
        return render(request, 'main/create_project.html', {'form': form})
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
  return render(request, 'main/project_list.html', {'projects':projects, 'can_create_project': can_create_project}) 


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
    return render(request, 'main/project_details.html', {'project': project, 'team': team, 'members': members, 'is_team_leader': is_team_leader, 'is_team_member':is_team_member})


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
            task.save()
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm()
    return render(request, 'main/create_task.html', {'form': form, 'project': project})


# list the task in each project
def task_list(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	tasks = project.task_set.all()
	return render(request, 'main/task_list.html', {'project': project, 'tasks': tasks})

# update task
def update_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'main/update_task.html', {'task':task, 'form': form, 'project_id': project_id, 'task_id': task_id})

# delete task
def delete_task(request, project_id, task_id):
	task = get_object_or_404(Task, pk=task_id)
	if request.method == 'POST':
		task.delete()
		return redirect('task_list', project_id=project_id)
	return render(request, 'main/delete_task.html', {'task':task, 'project_id': project_id, 'task_id': task_id})


# get task data for gantt chart
from django.http import JsonResponse

def get_tasks(request, project_id):
    # get_object_or_404() function to retrieve the project object with the given ID. If the object doesn't exist, it raises a Http404 exception.
    project = get_object_or_404(Project, pk=project_id)
    # filter() method of the Task model to retrieve all the tasks that belong to the project. 
	# set the project in Project to equal to project in the Task
	# The values() method is used to specify which fields of the Task model should be included in the queryset.
    tasks = Task.objects.filter(project=project).values('id','title', 'start_date', 'end_date')
    # creates an empty list data to store the JSON data for each task.
    data = []
    # iterates over each task in the queryset 
    for task in tasks:
	# and calculates the duration of the task by subtracting the start date from the end date and adding 1 (since the start and end dates are inclusive).
        start_date = task['start_date']
        end_date = task['end_date']
        duration = (end_date - start_date).days + 1
	
        data.append({
            'Task_ID': task['title'],
            'Task_Name': task['title'],
            'Start_Date': start_date.strftime('%Y-%m-%d'),
            'End_Date': end_date.strftime('%Y-%m-%d'),
            'Duration': duration,
            'Percent_Complete': 30,
            'Dependencies': None
        })
    return JsonResponse(data, safe=False)


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
    return render(request, 'main/team_list.html', {'teams': teams, 'my_teams': my_teams, 'can_create_team':can_create_team, 'can_update_team':can_update_team})

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
    return render(request, 'main/create_team.html', {'team_form': team_form, 'membership_form': membership_form})

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
            membership_form.save(team=team)
            return redirect('team_list')
    else:
        team_form = TeamForm(instance=team)
        membership_form = MembershipForm()
    return render(request, 'main/update_team.html', {'team_form': team_form, 'membership_form': membership_form, 'team': team})


# delete team
def delete_team(request, pk):
    if not request.user.groups.filter(name='team_manager').exists():
        raise PermissionDenied
    
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'main/delete_team.html', {'team': team, 'pk': pk})


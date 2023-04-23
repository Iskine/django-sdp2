from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PostForm, ProjectForm, TaskForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login, logout
from .models import Post, Project, TeamMember, Task
from django.contrib.auth.models import User, Group
from django.template import loader 
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView







#home page
@login_required(login_url="/login")#if not login, redirect to /login
def home(request): 
	posts = Post.objects.all()

	if request.method == "POST":
		post_id = request.POST.get("post-id")
		user_id = request.POST.get("user-id")

		if post_id:
			post = Post.objects.filter(id=post_id).first()
			if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
				post.delete()
		elif user_id:
			user = User.objects.filter(id=user_id).first()
			if user and request.user.is_staff:
				try: 
					group = Group.objects.get(name='student')
					group.user_set.remove(user)
				except: 
					pass 

				try: 
					group = Group.objects.get(name='advisor')
					group.user_set.remove(user)
				except: 
					pass
				
	return render(request, 'main/home.html', {"posts": posts})

#create a post form
@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request): 
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect("/home")
	else:
		form = PostForm()
	return render(request, 'main/create_post.html', {"form": form})

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

#the account owner can edit/update their profile information
@login_required(login_url="/login")
def edit_my_profile(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		form = RegisterForm(request.POST or None, instance=current_user)
		if form.is_valid():
			form.save()
			login(request, current_user)
			messages.success(request, ("Your Profile has been updated"))
			return redirect('my_profile')
		
		return render(request, "main/edit_my_profile.html", {'form':form})
	else:
		messages.success(request, ("You must logged in to edit profile"))
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
def edit_user(request, id):
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
	return render(request, 'main/edit_user.html', context)

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
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'main/create_project.html', {'form': form})


#display list of projects
@login_required(login_url="/login")
def project_list(request):
  projects = Project.objects.all().values()
  template = loader.get_template('main/project_list.html')
  context = {
    'projects': projects,
  }
  return HttpResponse(template.render(context, request))

# Delete project
@login_required(login_url="/login")
def delete_project(request, id):
	project_to_delete = Project.objects.get(id=id)
	if request.method == 'POST':
		project_to_delete.delete()
		return redirect('home')
	else:
		context = {
			'projects' : project_to_delete,
		}
	return render(request, 'main/delete_project.html', context)


# Create project task
def create_task(request, project_id):
    project = Project.objects.get(id=project_id)
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



# class GanttChartView(GoogleChartsMixin, JSONResponseMixin, TemplateView):
#     chart_type = 'gantt'
#     template_name = 'gantt_chart.html'

#     def get_context_data(self, **kwargs):
#         context = super(GanttChartView, self).get_context_data(**kwargs)
#         tasks = Task.objects.all()
#         data = []
#         for task in tasks:
#             data.append([
#                 task.title,
#                 task.title,
#                 '',
#                 task.start_date,
#                 task.end_date,
#                 None,
#                 100,
#                 ''
#             ])
#         context['chart_data'] = data
#         return context

from django.http import JsonResponse
from .models import Task

from django.utils.dateparse import parse_date

from datetime import datetime

def get_tasks(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project=project).values('title', 'start_date', 'end_date')
    data = []
    for task in tasks:
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



from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProjectForm, TaskForm, TeamForm, MembershipForm, SubTaskForm, CustomMyProfileUpdateForm, CustomUserForm ,CustomUserPasswordChangeForm, CommentForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from .models import Project, Task, Team, Membership, SubTask, Log, Comment
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
from django import forms 
from datetime import datetime, timedelta












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
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    user = User.objects.all().values()
    template = loader.get_template('frontend/myprofile.html')
    context = {
        'user': user, 
        'user_group_name': user_group_name
    }
    return HttpResponse(template.render(context, request))


#the account owner can update their profile information
@login_required(login_url="/login")
def update_my_profile(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = CustomMyProfileUpdateForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            return redirect('my_profile')
        return render(request, "frontend/updatemyprofile.html", {'form': form, 'user_group_name': user_group_name})
    else:
        messages.success(request, ("You must be logged in to update your profile"))
        return redirect('/login')
    


# Delete my profile
@login_required(login_url="/login")
def delete_my_account(request, id):
    
    user = User.objects.get(id=id)
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    if request.method == 'POST':
        user.delete()
        logout(request)
        return redirect('login')
    else: context = {
            'user': user,
            'user_group_name': user_group_name,
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
@login_required(login_url="/login")
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
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    mymembers = User.objects.all()
    template = loader.get_template('frontend/userlist.html')
    context = {
        'mymembers': mymembers,
        'user_group_name': user_group_name
    }
    return HttpResponse(template.render(context, request))



#display the user in details
@login_required(login_url="/login")
def details(request, id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    memberdetails = User.objects.get(id=id)
    template = loader.get_template('frontend/userdetails.html')
    context = {
        'memberdetails': memberdetails,
        'user_group_name': user_group_name
    }
    return HttpResponse(template.render(context, request))




# list member team
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def team_list(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        my_teams = teams
        can_create_team = False
        can_update_team = False
        user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        my_teams = teams
        can_create_team = False
        can_update_team = False
        user_group_name = 'Advisor'
        
    elif user.groups.filter(name='team_manager').exists():
        teams = Team.objects.all()
        my_teams = teams
        can_create_team = True
        can_update_team = True
        user_group_name = 'Dean'
    else:
        teams = Team.objects.all()
        my_teams = []
        can_create_team = False
        can_update_team = False
        user_group_name = 'Admin'
    return render(request, 'frontend/teamlist.html', {'teams': teams, 'my_teams': my_teams, 'can_create_team':can_create_team, 'can_update_team':can_update_team, 'user_group_name': user_group_name})





#create team
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def create_team(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    if not request.user.groups.filter(name='team_manager').exists():
        raise PermissionDenied

    if request.method == 'POST':

        team_form = TeamForm(request.POST)
        membership_form = MembershipForm(request.POST)
        if team_form.is_valid() and membership_form.is_valid():
            team = team_form.save()
            membership_form.save(team=team)

            # Create pre-made projects, tasks, and subtasks for the new team
            projects = [
                {
                    'name': 'SDP 1',
                    'description': 'Senior Development Project 1',
                    'start_date': datetime(2023, 8, 1),
                    'end_date': datetime(2023, 8, 1) + timedelta(days=90),
                    'status': 'Pending',
                    'team': team,
                    'created_by': request.user,
                },
                 {
                    'name': 'SDP 2',
                    'description': 'Senior Development Project 2',
                    'start_date': datetime(2024, 1, 1),
                    'end_date':  datetime(2024, 1, 1) + timedelta(days=90),
                    'status': 'Pending',
                    'team': team,
                    'created_by': request.user,
                },
                
                # Add more projects here
            ]
            for project_data in projects:
                project = Project.objects.create(**project_data)

                tasks = [
                    {
                        'title': 'Proposal Draft',
                        'description': "A one-page document for your project's idea.",
                        'project': project,
                        'start_date': datetime(2023, 8, 1),
                        'end_date': datetime(2023, 8, 1) + timedelta(days=14),
                        'created_by': request.user,# Set to the user who will create the task
                        'subtasks': [
                                {
                                    'title': 'One-page proposal',
                                    'description': '1-page document explaining your project description, project stakeholders, main objectives, specific objectives, benefit of client, and technology in use.',
                                    'start_date': datetime(2023, 8, 1),
                                    'end_date': datetime(2023, 8, 1) + timedelta(days=14),
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                        ]  
                    },
                    {
                        'title': 'Senior Project Development Document',
                        'description': 'Detailed Documentation of Your SDP',
                        'project': project,
                        'start_date': datetime(2023, 8, 17),
                        'end_date': datetime(2023, 8, 17) + timedelta(days=90),
                        'created_by': request.user,  # Set to the user who will create the task
                        'subtasks': [
                                {
                                    'title': 'Introduction',
                                    'description': 'Description of the problem',
                                    'start_date': datetime(2023, 8, 17),
                                    'end_date': datetime(2023, 8, 17) + timedelta(days=2),
                                 
                                    'created_by': request.user,  # Set to the user who will create the subtask
                            },
                            {
                                    'title': 'Project Objectives',
                                    'description': 'General and specific objectives',
                                    'start_date': datetime(2023, 8, 19),
                                    'end_date': datetime(2023, 8, 19) + timedelta(days=1),
                                
                                    'created_by': request.user,  # Set to the user who will create the subtask
                            },
                            {
                                    'title': 'General Objectives',
                                    'description': 'General Objectives',
                                    'start_date': datetime(2023, 8, 19),
                                    'end_date': datetime(2023, 8, 19) + timedelta(days=1),
                                   
                                    'created_by': request.user,  # Set to the user who will create the subtask
                            },
                            {
                                    'title': 'Specific Objectives',
                                    'description': 'Measureable objectives',
                                    'start_date': datetime(2023, 8, 19),
                                    'end_date': datetime(2023, 8, 19) + timedelta(days=1),
                           
                                    'created_by': request.user,  # Set to the user who will create the subtask
                            },
                            {
                                    'title': 'Related Works',
                                    'description': 'Description of similar solutions',
                                    'start_date': datetime(2023, 8, 20),
                                    'end_date': datetime(2023, 8, 20) + timedelta(days=1),
                                 
                                
                                    'created_by': request.user,  # Set to the user who will create the subtask
                            },
                            {
                                    'title': 'Preliminary Investigation',
                                    'description': 'Preliminary Investatgation',
                                    'start_date': datetime(2023, 8, 21),
                                            'end_date': datetime(2023, 8, 21) + timedelta(days=1),
                         
                           
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Company Profile',
                                    'description': 'name; address; line of business; company contact; stakeholder',
                                    'start_date': datetime(2023, 8, 22),
                                    'end_date': datetime(2023, 8, 22) + timedelta(days=1),
                               
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Organizational Chart',
                                    'description': 'Chart of organization',
                                    'start_date': datetime(2023, 8, 22),
                                    'end_date': datetime(2023, 8, 22) + timedelta(days=1),
                        
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Statement of the Mission',
                                    'description': 'if any please write it down',
                                    'start_date': datetime(2023, 8, 23),
                                    'end_date': datetime(2023, 8, 23) + timedelta(days=1),
                          
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Project Request',
                                    'description': 'How the project was initiated',
                                    'start_date': datetime(2023, 8, 24),
                                    'end_date': datetime(2023, 8, 24) + timedelta(days=1),
                
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Description of the Problem',
                                    'description': 'description of the problem to be investigated',
                                    'start_date': datetime(2023, 8, 25),
                                    'end_date': datetime(2023, 8, 25) + timedelta(days=1),
                                 
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Project Scopes and Constraints',
                                    'description': 'Project Scopes and Constraints',
                                    'start_date': datetime(2023, 8, 26),
                                    'end_date': datetime(2023, 8, 26) + timedelta(days=5),
                           
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Expected Business Benefits',
                                    'description': 'Expected Business Benefits',
                                    'start_date': datetime(2023, 9, 1),
                                    'end_date': datetime(2023, 9, 1) + timedelta(days=3),
                 
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Development Environment',
                                    'description': 'Details of the methodology, model, languages',
                                    'start_date': datetime(2023, 9, 5),
                                    'end_date': datetime(2023, 9, 5) + timedelta(days=3),
                       
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Feasibility Study',
                                    'description': 'Feasibility Study',
                                    'start_date': datetime(2023, 9, 9),
                                    'end_date': datetime(2023, 9, 9) + timedelta(days=1),
                   
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Technical Feasibility',
                                    'description': 'Technical Feasibility',
                                    'start_date': datetime(2023, 9, 10),
                                    'end_date': datetime(2023, 9, 10) + timedelta(days=2),
                    
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Legal Feasibility',
                                    'description': 'Legal Feasibility',
                                    'start_date': datetime(2023, 9, 12),
                                    'end_date': datetime(2023, 9, 12) + timedelta(days=2),
                                
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Operational Feasibility',
                                    'description': 'Operational Feasibility',
                                    'start_date': datetime(2023, 9, 14),
                                    'end_date': datetime(2023, 9, 14) + timedelta(days=2),
                         
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Schedule Feasibility',
                                    'description': 'ref.toAppendix-Software Cost Estimation',
                                    'start_date': datetime(2023, 9, 16),
                                    'end_date': datetime(2023, 9, 16) + timedelta(days=2),
                       
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Financial Feasibility',
                                    'description': 'ref.toAppendix-Software Cost Estimation',
                                    'start_date': datetime(2023, 9, 18),
                                    'end_date': datetime(2023, 9, 18) + timedelta(days=2),
                              
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Planning',
                                    'description': 'Gantt chart',
                                    'start_date': datetime(2023, 9, 20),
                                    'end_date': datetime(2023, 9, 20) + timedelta(days=5),
                                
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Analysis and Design',
                                    'description': 'Analysis and Design',
                                    'start_date': datetime(2023, 9, 25),
                                    'end_date': datetime(2023, 9, 25) + timedelta(days=20),
                               
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': "Design's Introduction",
                                    'description': "Design's Introduction",
                                    'start_date': datetime(2023, 10, 16),
                                    'end_date': datetime(2023, 10, 16) + timedelta(days=1),
                                
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Risk Analysis',
                                    'description': 'spiral ref.Appendix -Software Cost Estimation',
                                    'start_date': datetime(2023, 10, 17),
                                    'end_date': datetime(2023, 10, 17) + timedelta(days=4),
                             
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Conduct of Analysis',
                                    'description': 'analysis method',
                                    'start_date': datetime(2023, 10, 22),
                                    'end_date': datetime(2023, 10, 22) + timedelta(days=4),
                                    
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'User Requirements',
                                    'description': 'output Requirements',
                                    'start_date': datetime(2023, 10, 27),
                                    'end_date': datetime(2023, 10, 27) + timedelta(days=1),
                           
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                },
                            {
                                    'title': 'Infrastructure Analysis',
                                    'description': 'Infrastructure Analysis',
                                    'start_date': datetime(2023, 10, 29),
                                    'end_date': datetime(2023, 10, 29) + timedelta(days=1),
                                
                                    
                                    'created_by': request.user,  # Set to the user who will create the subtask
                                }
                        ]  
                        
                    },
                    # Add more tasks here
                ]
                
                for task_data in tasks:
                    task_subtasks = task_data.pop('subtasks', [])  # Remove the 'subtasks' key from task_data and store it in a variable
                    task = Task.objects.create(**task_data)
                    for subtask_data in task_subtasks:
                        subtask_data['task'] = task  # Add the task to the subtask data
                        SubTask.objects.create(**subtask_data)
                    

            return redirect('team_list')
    else:
        team_form = TeamForm()
        membership_form = MembershipForm()

    teams = Team.objects.all()
    memberships = Membership.objects.all()
    team_managers = Group.objects.get(name='team_manager').user_set.all()

    return render(request, 'frontend/createteam.html', {'team_form': team_form, 'membership_form': membership_form, 'teams': teams, 'memberships': memberships, ' team_managers':  team_managers, 'user_group_name' : user_group_name})




#update team
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def update_team(request, pk):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
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
    return render(request, 'frontend/updateteam.html', {'team_form': team_form, 'membership_form': membership_form, 'team': team, 'user_group_name': user_group_name})






# delete team
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def delete_team(request, pk):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    if not request.user.groups.filter(name='team_manager').exists():
        raise PermissionDenied
    
    team = get_object_or_404(Team, pk=pk)
    # team = Team.objects.all()
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'frontend/deleteteam.html', {'team': team, 'pk': pk, 'user_group_name': user_group_name})




#create new project
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def create_project(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    if user.groups.filter(name='team_member').exists() or user.groups.filter(name='team_leader').exists():
        if request.method == 'POST':
            form = ProjectForm(user=user, data=request.POST)
            if form.is_valid():
                project = form.save(commit=False)
                project.created_by = request.user
                project.save()
                

                team = form.cleaned_data.get('team')
                team_name = team.name if team else ""
                log_action = f"Project: '{project.name}' created by '{request.user}' for team '{team_name}'"
                create_log(request.user, None, project.id, None, log_action, project.description, team=team)

                
                return redirect('project_list')
        else:
            form = ProjectForm(user=user)

        return render(request, 'frontend/createproject.html', {'form': form,   'user_group_name': user_group_name})
    else: 
        raise PermissionDenied








#display list of projects
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def project_list(request):
  user = request.user
  if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        projects = Project.objects.filter(Q(team__in=teams) | Q(created_by=user))
        can_create_project = True
        can_see_all_project = False
        user_group_name = 'Student'
  elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        projects = Project.objects.filter(Q(team__in=teams) | Q(created_by=user))
        can_create_project = True
        can_see_all_project = True
        user_group_name = 'Advisor'
  elif user.groups.filter(name='team_manager').exists():
        teams = Team.objects.all()
        projects = Project.objects.filter(team__in=teams)
        can_create_project = False
        can_see_all_project = True
        user_group_name = 'Dean'
  else:
        projects = Project.objects.filter(created_by=user)
        can_create_project = False
        can_see_all_project = False
        user_group_name = 'Admin'
  return render(request, 'frontend/projectlist.html', {'user_group_name': user_group_name, 'projects':projects, 'can_create_project': can_create_project, 'can_see_all_project': can_see_all_project}) 










@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def project_list_all(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    if user.groups.filter(name='team_manager').exists() or user.groups.filter(name='team_leader').exists():
        projects = Project.objects.exclude(team=None)
        return render(request, 'frontend/projectlistall.html', {'projects': projects, 'user_group_name': user_group_name})
    else:
        raise PermissionDenied
    # projects = Project.objects.all()
    # return render(request, 'frontend/projectlistall.html', {'projects': projects})




# project details
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def project_details(request, project_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
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
    return render(request, 'frontend/projectdetails.html', {'project': project, 'team': team, 'members': members, 'is_team_leader': is_team_leader, 'is_team_member':is_team_member, 'user_group_name': user_group_name})






# Update Project
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def update_project(request, project_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    project = get_object_or_404(Project, pk=project_id)

    # Check if user is authorized to update project
    user = request.user
    if not user.groups.filter(Q(name='team_leader') | Q(name='team_member')).exists() and user != project.created_by:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(data=request.POST, instance=project, user=user)
        if form.is_valid():
            form.save()

    
            team = form.cleaned_data['team']
            team_name = team.name if team else ""
            log_action = f"Project: '{project.name}' updated for team '{team_name}' by '{request.user}'"
            create_log(request.user, None, project.id, None, log_action, project.description, team=team)

            # team_name = form.cleaned_data['team'].name if form.cleaned_data['team'] else "No team"
            # log_action = f"Project: '{project.name}' updated for team '{team_name}' by {user.username}"
            # create_log(project, user, log_action, {project.description})

            return redirect('project_details', project_id=project.pk)
    else:
        form = ProjectForm(instance=project, user=user)
        form.fields['description'].widget = forms.Textarea(attrs={'rows': 3})
        form.fields['start_date'].widget.attrs.update({'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-10 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'})
        form.fields['end_date'].widget.attrs.update({'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-10 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'})
    return render(request, 'frontend/updateproject.html', {'form': form, 'project': project, 'user_group_name': user_group_name})



# Delete project
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def delete_project(request, project_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
        user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
        user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
        user_group_name = 'Dean'
    else:
        user_group_name = 'Admin'

    
    project = get_object_or_404(Project, pk=project_id)
    if not user.groups.filter(Q(name='team_leader') | Q(name='team_member')).exists() and user != project.created_by:
        raise PermissionDenied

    if request.method == 'POST':
        project.delete()


        return redirect('project_list')

    return render(request, 'frontend/deleteproject.html', {'project': project, 'user_group_name': user_group_name})





# Create project task
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def create_task(request, project_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    project = Project.objects.get(id=project_id)

    if not (request.user.groups.filter(name='team_member').exists() or request.user.groups.filter(name='team_leader').exists()):
         raise PermissionDenied
         
    if request.method == 'POST':
        form = TaskForm(request.POST or None, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()

       
            team = form.cleaned_data.get('team')
            team_name = team.name if team else ""
            log_action = f"Task: '{task.title}' created for team '{team_name}' in project '{project.name}' by '{request.user}'"
            create_log(request.user, task, project.id, None, log_action, project.description, team=team)

            # team_name = project.team.name if project.team else "No team"
            # log_action = f"Task: '{task.title}' created for team '{team_name}' in project '{project.name}' by '{request.user.username}' "
            # create_log(project, task, log_action, {project.description})


            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm(project=project)
    return render(request, 'frontend/createtask.html', {'form': form, 'project': project, 'user_group_name': user_group_name})





# list the task in each project
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def task_list(request, project_id):

    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    project = get_object_or_404(Project, pk=project_id)
    tasks = project.tasks.all()
    is_team_member = request.user.groups.filter(name='team_member').exists()
    is_team_leader = request.user.groups.filter(name='team_leader').exists()
    return render(request, 'frontend/tasklist.html', {'project': project, 'tasks': tasks, 'is_team_member': is_team_member, 'is_team_leader': is_team_leader, 
		  'user_group_name': user_group_name})




# Task details
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def task_details(request, project_id, task_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id)
    # Check if the current user is a team leader
    is_team_leader = request.user.groups.filter(name='team_leader').exists()
    # Check if the current user is a team member
    is_team_member = request.user.groups.filter(name='team_member').exists()
    return render(request, 'frontend/taskdetails.html', {'project': project, 'task': task, 'members': members, 'is_team_leader': is_team_leader, 'is_team_member':is_team_member, 
		  'user_group_name': user_group_name})






# update task
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def update_task(request, project_id, task_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    project = task.project

    if not (request.user.groups.filter(name='team_member').exists() or request.user.groups.filter(name='team_leader').exists()):
        raise PermissionDenied

    # Allow all users in the project to update task
    elif project and ((user == project.created_by) or (project.team and user in project.team.members.all()) or Membership.objects.filter(team=project.team, user=user).exists() or user.groups.filter(name='team_leader').exists()):
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()

                team = form.cleaned_data.get('team')
                team_name = team.name if team else ""
                log_action = f"Task: '{task.title}' updated for team '{team_name}' in project '{project.name}' by '{request.user}'"
                create_log(request.user, task, project.id, None, log_action, project.description, team=team)

                # team_name = project.team.name if project.team else "No team"
                # log_action = f"Task: '{task.title}' updated for team '{team_name}' in project '{project.name}' by {request.user.username}"
                # create_log(project, task, log_action, {project.description})

                return redirect('task_list', project_id=project_id)
        else:
            form = TaskForm(instance=task, project=project, task=task)
            is_team_member = request.user.groups.filter(name='team_member').exists()
            is_team_leader = request.user.groups.filter(name='team_leader').exists()
            form.fields['description'].widget = forms.Textarea(attrs={'rows': 3})
            form.fields['start_date'].widget.attrs.update({'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-10 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'})
            form.fields['end_date'].widget.attrs.update({'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-10 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'})
        
        return render(request, 'frontend/updatetask.html', {'task':task, 'form': form, 'project_id': project_id, 'task_id': task_id, 'is_team_member': is_team_member, 'is_team_leader': is_team_leader, 
		  'user_group_name': user_group_name})
    else:
        return HttpResponseForbidden()



# delete task
@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    # Check if the current user is a team leader
    is_team_leader = user.groups.filter(name='team_leader').exists()
    is_team_member = user.groups.filter(name='team_member').exists()


    # # Only allow team leaders to delete tasks
    if is_team_member and not is_team_leader:
        raise PermissionDenied

    if not is_team_member and not is_team_leader:
        raise PermissionDenied

    if request.method == 'POST':
        task.delete()
        return redirect('task_list', project_id=project_id)

    return render(request, 'frontend/deletetask.html', {'task':task, 'project_id': project_id, 'task_id': task_id, 'is_team_leader': is_team_leader, 'is_team_member': is_team_member, 'user_group_name': user_group_name})



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

@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
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









from django.http import JsonResponse
from django.db.models import Count

@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def get_sub_tasks(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id, project__id=project_id)
    subtasks = SubTask.objects.filter(task=task).values('id','title', 'start_date', 'end_date', 'completed')
    data = []
    for subtask in subtasks:
        data.append({
            'SubTask_ID': subtask['id'],
            'SubTask_Name': subtask['title'],
            'Start_Date': subtask['start_date'].strftime('%Y-%m-%d'),
            'End_Date': subtask['end_date'].strftime('%Y-%m-%d'),
            'Percent_Complete': 100 if subtask['completed'] else 0,
            'Dependencies': None
        })

    return JsonResponse(data, safe=False)













from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import SubTask, Task
from .forms import SubTaskForm

@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def create_sub_task(request, task_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    task = get_object_or_404(Task, pk=task_id)
    project = task.project
    user = request.user

    if not (user == project.created_by or (project.team and user in project.team.members.all()) or Membership.objects.filter(team=project.team, user=user).exists() or Team.objects.filter(team_leader=user)):
        return HttpResponseForbidden("You don't have permission to create subtasks in this task.")

    if request.method == "POST":
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.created_by = request.user
            subtask.task = task
            subtask.save()

            team = form.cleaned_data.get('team')
            team_name = team.name if team else ""
            log_action = f"Sub Task: '{subtask.title}' created for team '{team_name}' in project '{project.name}' in task '{task.title}' by '{request.user}'"
            create_log(request.user, task, project.id, subtask, log_action, project.description, team=team)


            return redirect("sub_task_list", project_id=project.id, task_id=task.id)  # Assuming you have a sub_task_list view
    else:
        form = SubTaskForm()

    context = {
        "task_id": task_id,
        "project_id": project.id,
        "form": form,
        "task": task,
        'user_group_name': user_group_name
    }

    return render(request, 'frontend/createsubtask.html', context)



@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def sub_task_list(request, project_id, task_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, project=project)

    if not (request.user.groups.filter(name='team_member').exists() or request.user.groups.filter(name='team_leader').exists() or request.user.groups.filter(name='team_manager').exists()):
        raise PermissionDenied

    
    sub_tasks = SubTask.objects.filter(task=task)

    is_team_member = request.user.groups.filter(name='team_member').exists()
    is_team_leader = request.user.groups.filter(name='team_leader').exists()

    return render(request, 'frontend/subtasklist.html', {'sub_tasks': sub_tasks, 'project_id': project_id, 'task_id': task_id, 'project': project, 'task': task, 'is_team_member': is_team_member, 'is_team_leader': is_team_leader, 'user_group_name': user_group_name})







@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def update_sub_task(request, project_id, task_id, sub_task_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'

    sub_task = get_object_or_404(SubTask, pk=sub_task_id)
    task = sub_task.task
    project = get_object_or_404(Project, pk=project_id)

    # Check user permissions
    is_team_member = user.groups.filter(name='team_member').exists()
    team_leader = Team.objects.filter(team_leader=user).exists()

    if not (is_team_member or team_leader):
        raise PermissionDenied("You do not have permission to access this page")


    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=sub_task)
        if form.is_valid():
            form.save()


            team = form.cleaned_data.get('team')
            subtask = sub_task
            team_name = team.name if team else ""
            log_action = f"Sub Task: '{subtask.title}' updated for team '{team_name}' in project '{project.name}' in task '{task.title}' by '{request.user}'"
            create_log(request.user, task, project.id, subtask, log_action, project.description, team=team)


            return redirect('sub_task_list', project_id=project.id, task_id=task.id)
    else:
        form = SubTaskForm(instance=sub_task)
        form.fields['description'].widget = forms.Textarea(attrs={'rows': 3})
        form.fields['start_date'].widget.attrs.update({'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-10 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'})
        form.fields['end_date'].widget.attrs.update({'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-10 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'})
    

    context = {
        'form': form,
        'sub_task_id': sub_task_id,
        'project_id': project_id,
        'task_id': task_id,
        'sub_task': sub_task,
        'user_group_name': user_group_name
    }

    return render(request, 'frontend/updatesubtask.html', context)





@login_required(login_url="/login")
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
def delete_sub_task(request, sub_task_id, project_id, task_id):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'
    sub_task = get_object_or_404(SubTask, pk=sub_task_id)
    task = sub_task.task
    project = task.project

    # Check user permissions
    if not (request.user == project.created_by or (project.team and request.user in project.team.members.all()) or Membership.objects.filter(team=project.team, user=request.user).exists() or Team.objects.filter(team_leader=user)):
        return HttpResponseForbidden("You don't have permission to delete subtasks in this project.")

    if request.method == 'POST':
        sub_task.delete()
        return redirect('sub_task_list', project_id=project.id, task_id=task.id)

    context = {
        'sub_task_id': sub_task_id,
        'project_id': project_id,
        'task_id': task_id,
        'sub_task': sub_task,
        'user_group_name': user_group_name
    }

    return render(request, 'frontend/deletesubtask.html', context)





def create_log(user, task, project_id, subtask, log_action, comment='', team=None):
    project = Project.objects.get(pk=project_id)
    log = Log(user=user, project=project, task=task, subtask=subtask, log_action=log_action, comment=comment, team=team)
    log.save()


def display_log(request):
    logs = Log.objects.all()
    return render(request, 'frontend/comment.html', {'logs': logs})



@login_required(login_url="/login")
def comment(request):
    user = request.user
    if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        team_users = User.objects.filter(membership__team__in=teams)
        comments = Comment.objects.filter(user__in=team_users)
    elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        team_users = User.objects.filter(membership__team__in=teams)
        comments = Comment.objects.filter(user__in=team_users)
    else:
        comment = None

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('comment')
    else: 
        form = CommentForm()

    return render(request, 'frontend/comment.html', {'comments': comments, 'form': form})




@login_required(login_url="/login")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # You can add a check to ensure the user deleting the comment is the owner of the comment
    if request.user != comment.user:
        raise PermissionDenied

    if request.method == 'POST':
        comment.delete()
        return redirect('comment')




def delete_log(request, log_id):
    log = get_object_or_404(Log, id=log_id)
   
    if request.method == 'POST':
        log.delete()
        return redirect('comment')




# #comments works 
# def comments_and_logs(request, log_id=None):
#     user = request.user

#     # filter comments based on user type
#     if user.groups.filter(name='team_member').exists():
#         memberships = Membership.objects.filter(user=user)
#         teams = [membership.team for membership in memberships]
#         team_users = User.objects.filter(membership__team__in=teams)
#         comments = Comment.objects.filter(user__in=team_users)
#     elif user.groups.filter(name='team_leader').exists():
#         teams = Team.objects.filter(team_leader=user)
#         team_users = User.objects.filter(membership__team__in=teams)
#         comments = Comment.objects.filter(user__in=team_users)
#     else:
#         comments = None

#     # filter logs based on user type
#     if user.groups.filter(name='team_member').exists():
#         memberships = Membership.objects.filter(user=user)
#         teams = [membership.team for membership in memberships]
#         team_users = User.objects.filter(membership__team__in=teams)
#         logs = Log.objects.filter(user__in=team_users)
#     elif user.groups.filter(name='team_leader').exists():
#         team = Team.objects.filter(team_leader=user).first()
#         memberships = Membership.objects.filter(team=team)
#         team_users = User.objects.filter(membership__in=memberships)
#         logs = Log.objects.filter(team=team)
#         # create a new log if it doesn't already exist for the current team leader
#         if not logs.exists():
#             log = Log.objects.create(
#                 user=user,
#                 team=team
#             )
#             # set the users associated with the team to the log's user field
#             log.user.set(team_users)
#             log.save()
#     else:
#         logs = None

#     # handle comment form submission
#     form = CommentForm()
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.save()
#             # add the newly created comment to the comments queryset
#             comments |= Comment.objects.filter(pk=comment.pk)

#     # handle log deletion
#     if log_id:
#         log = get_object_or_404(Log, id=log_id)
#         log.delete()
#         return redirect('comment')

#     return render(request, 'frontend/comment.html', {'comments': comments, 'logs': logs, 'form': form})








def comments_and_logs(request, log_id=None):
    user = request.user
    if user.groups.filter(name='team_member').exists():
            user_group_name = 'Student'
    elif user.groups.filter(name='team_leader').exists():
            user_group_name = 'Advisor'
    elif user.groups.filter(name='team_manager').exists():
            user_group_name = 'Dean'
    else:
            user_group_name = 'Admin'




    # filter comments based on user type
    if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        team_users = User.objects.filter(membership__team__in=teams)
        comments = Comment.objects.filter(user__in=team_users)
    elif user.groups.filter(name='team_leader').exists():
        teams = Team.objects.filter(team_leader=user)
        team_users = User.objects.filter(membership__team__in=teams)
        comments = Comment.objects.filter(user__in=team_users)
    else:
        comments = None

    # filter logs based on user type
    if user.groups.filter(name='team_member').exists():
        memberships = Membership.objects.filter(user=user)
        teams = [membership.team for membership in memberships]
        team_users = User.objects.filter(membership__team__in=teams)
        logs = Log.objects.all()  # remove filtering to show all logs
    elif user.groups.filter(name='team_leader').exists():
        team = Team.objects.filter(team_leader=user).first()
        memberships = Membership.objects.filter(team=team)
        team_users = User.objects.filter(membership__in=memberships)
        logs = Log.objects.exclude(team=None)  # remove filtering to show all logs
    else:
        logs = None
    
  
    # handle comment form submission
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            # add the newly created comment to the comments queryset
            comments |= Comment.objects.filter(pk=comment.pk)

    # handle log deletion
    if log_id:
        log = get_object_or_404(Log, id=log_id)
        log.delete()
        return redirect('comment')
    

    return render(request, 'frontend/comment.html', {'comments': comments, 'logs': logs, 'form': form, 	  'user_group_name': user_group_name})






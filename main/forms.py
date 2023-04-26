from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Project, Task, Team, Membership

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class ProjectForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('complete', 'Complete')
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    team = forms.ModelChoiceField(queryset=Team.objects.none())

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'team']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(team_leader=user)
 

class TaskForm(forms.ModelForm):
        start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
        end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
        class Meta:
            model = Task
            fields = ['title', 'description', 'assignee','start_date', 'end_date']
            widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
             
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['assignee'].required = False


class TeamForm(forms.ModelForm):
    team_leader = forms.ModelChoiceField(queryset=User.objects.none())
    team_manager = forms.ModelChoiceField(queryset=User.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_leader'].queryset = Group.objects.get(name='team_leader').user_set.all()
        self.fields['team_manager'].queryset = Group.objects.get(name='team_manager').user_set.all()

    class Meta:
        model = Team
        fields = ['name', 'team_leader', 'team_manager']

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
        return team
    


class MembershipForm(forms.Form):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = Group.objects.get(name='team_member').user_set.all()

    class Meta:
        model = Membership
        fields = ['members']

    def save(self, commit=True, team=None):
        for user in self.cleaned_data['members']:
            membership = Membership(team=team, user=user)
            if commit:
                membership.save()
        return membership


from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from .models import Project, Task, Team, Membership, SubTask
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
import re
from django.forms.widgets import HiddenInput
from django.contrib.auth import password_validation



class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'transition-colors duration-300 ease-in mt-1 pl-2 px-14 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-sky-500 w-full rounded-md sm:text-md focus:ring-1 mb-4', 'placeholder': 'Josuke'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'transition-colors duration-300 ease-in mt-1 pl-2 px-14 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-sky-500 w-full rounded-md sm:text-md focus:ring-1 mb-4', 'placeholder': 'Joestar'}))
    username = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'transition-colors duration-300 ease-in mt-1 pl-2 px-14 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-sky-500 w-full rounded-md sm:text-md focus:ring-1 mb-4', 'placeholder': 'JoJo'}))
    email = forms.EmailField(required=True,  widget=forms.TextInput(attrs={'class': 'transition-colors duration-300 ease-in mt-1 pl-2 pr-2 px-14 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-sky-500 w-full rounded-md sm:text-md focus:ring-1 mb-4', 'placeholder': '202000999@my.apiu.edu'}))
    password1 = forms.CharField(required=True,  widget=forms.PasswordInput(attrs={'class': 'transition-colors duration-300 ease-in mt-1 pl-2  px-14 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-sky-500 w-full rounded-md sm:text-md focus:ring-1 mb-4', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True,  widget=forms.PasswordInput(attrs={'class': 'transition-colors duration-300 ease-in mt-1 pl-2 px-14 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-sky-500 w-full rounded-md sm:text-md focus:ring-1 mb-4', 'placeholder': 'Re-type Password'}))

    def clean_email(self):
        value = self.cleaned_data.get('email')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise forms.ValidationError("Please enter a valid email address. It should contain '@' and a domain name.")
        return value

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]




class CustomMyProfileUpdateForm(UserChangeForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomMyProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'input_type': 'password'})
        self.fields['password2'].widget.attrs.update({'input_type': 'password'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != '' and password1 != password2:
            raise forms.ValidationError('The two password fields did not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user








class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
        ]
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].required = False
        self.fields['is_staff'].required = False
        self.fields['is_superuser'].required = False
        self.fields['groups'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if 'groups' in self.cleaned_data:
                user.groups.set(self.cleaned_data['groups'])
        return user







class CustomUserPasswordChangeForm(UserChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields.pop('first_name')
        self.fields.pop('last_name')
        self.fields.pop('email')
        self.fields.pop('is_staff')
        self.fields.pop('is_superuser')
        self.fields.pop('groups')
        self.fields.pop('user_permissions')
        self.fields.pop('last_login')
        self.fields.pop('date_joined')
        self.fields.pop('is_active')
        self.fields['password'].required = False

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_('Passwords do not match'))
        return new_password2

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
            if commit:
                user.save()
        return user
    



class ProjectForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Completed', 'Completed')
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    team = forms.ModelChoiceField(queryset=Team.objects.none(), required=False)

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






class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'completed',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
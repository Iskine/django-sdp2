from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Project, Task

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ["title", "description"]


class ProjectForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('complete', 'Complete')
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


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
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone



class Team(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateField(default=timezone.now, null=False)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leading_teams', null=True)
    team_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_teams', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='teams', blank=True)

    def __str__(self):
        return self.name
    

class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.name} | {self.user.username}'


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
   
    def __str__(self):
        return self.name
    

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', blank=True, null=True )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


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
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_tasks')
    percent_complete = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def update_percent_complete(self):
        """
        Update the percent complete of the task based on the completion status of its sub-tasks.
        """
        num_sub_tasks = self.sub_tasks.count()
        if num_sub_tasks == 0:
            self.percent_complete = 0
        else:
            num_completed_sub_tasks = self.sub_tasks.filter(completed=True).count()
            self.percent_complete = int((num_completed_sub_tasks / num_sub_tasks) * 100)
        self.save()


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_sub_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sub_tasks')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.task.update_percent_complete()
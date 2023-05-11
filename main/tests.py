# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User, Group
# from main.models import Team, Project
# from datetime import datetime, timedelta

# class CreateProjectViewTest(TestCase):

#     def setUp(self):
#         # Create a user, group and team for testing
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.group = Group.objects.create(name='team_member')
#         self.group.user_set.add(self.user)
#         self.team = Team.objects.create(name='Test Team', team_leader=self.user)

#         # Create a client and set login details
#         self.client = Client()
#         self.client.login(username='testuser', password='12345')

#         # Set project data
#         self.project_data = {
#             'name': 'Test Project',
#             'description': 'This is a test project',
#             'start_date': datetime.now().date(),
#             'end_date': (datetime.now() + timedelta(days=10)).date(),
#             'status': 'Pending',
#             'team': self.team.id
#         }

#     def test_create_project_view_with_valid_data(self):
#         # Get the create project url and post the data
#         url = reverse('create_project')
#         response = self.client.post(url, self.project_data)

#         # Assert that the project was created and the user was redirected
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Project.objects.count(), 1)
#         self.assertEqual(Project.objects.first().name, self.project_data['name'])

#     def test_create_project_view_with_invalid_data(self):
#         # Remove the required 'name' field from project_data
#         self.project_data.pop('name')

#         # Get the create project url and post the data
#         url = reverse('create_project')
#         response = self.client.post(url, self.project_data)

#         # Assert that the project was not created and the form is not valid
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Project.objects.count(), 0)
#         self.assertContains(response, 'This field is required.')
        
#     def test_create_project_view_with_unauthorized_user(self):
#         # Remove the user from the group to make them unauthorized
#         self.group.user_set.remove(self.user)

#         # Get the create project url and try to post the data
#         url = reverse('create_project')
#         response = self.client.post(url, self.project_data)

#         # Assert that the user is unauthorized and cannot create a project
#         self.assertEqual(response.status_code, 403)
#         self.assertEqual(Project.objects.count(), 0)



# class CreateTaskViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.group = Group.objects.create(name='team_member')
#         self.group.user_set.add(self.user)
#         self.project = Project.objects.create(name='Test Project', description='This is a test project', start_date=timezone.now(), end_date=timezone.now())
#         self.url = reverse('create_task', kwargs={'project_id': self.project.pk})

#     def test_create_task_view_with_authenticated_user(self):
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'frontend/createtask.html')

#         data = {
#             'title': 'Test Task',
#             'description': 'This is a test task',
#             'start_date': timezone.now(),
#             'end_date': timezone.now(),
#         }
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Task.objects.count(), 1)
#         task = Task.objects.first()
#         self.assertEqual(task.title, data['title'])
#         self.assertEqual(task.description, data['description'])
#         self.assertEqual(task.project, self.project)
#         self.assertEqual(task.created_by, self.user)

#     def test_create_task_view_with_unauthenticated_user(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, '/login/?next=' + self.url)

#     def test_create_task_view_with_unauthorized_user(self):
#         self.user.groups.clear()
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 403)



from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Project, Task, SubTask, Team

class CreateSubTaskViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(name='Test Team', team_leader=self.user)
        self.project = Project.objects.create(name='Test Project', created_by=self.user, team=self.team)
        self.task = Task.objects.create(title='Test Task', description='Test Description', project=self.project, created_by=self.user)
        
    def test_create_sub_task_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_sub_task', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/createsubtask.html')
        
        data = {
            'title': 'Test Sub Task',
            'description': 'Test Sub Task Description',
            'due_date': '2023-12-31',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.subtasks.count(), 1)
        
    def test_create_sub_task_unauthenticated(self):
        url = reverse('create_sub_task', args=[self.task.id])
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next={url}')
        response = self.client.post(url)
        self.assertRedirects(response, f'/login/?next={url}')

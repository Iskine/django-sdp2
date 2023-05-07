from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import Team, Project
from datetime import datetime, timedelta

class CreateProjectViewTest(TestCase):

    def setUp(self):
        # Create a user, group and team for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group.objects.create(name='team_member')
        self.group.user_set.add(self.user)
        self.team = Team.objects.create(name='Test Team', team_leader=self.user)

        # Create a client and set login details
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Set project data
        self.project_data = {
            'name': 'Test Project',
            'description': 'This is a test project',
            'start_date': datetime.now().date(),
            'end_date': (datetime.now() + timedelta(days=10)).date(),
            'status': 'Pending',
            'team': self.team.id
        }

    def test_create_project_view_with_valid_data(self):
        # Get the create project url and post the data
        url = reverse('create_project')
        response = self.client.post(url, self.project_data)

        # Assert that the project was created and the user was redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, self.project_data['name'])

    def test_create_project_view_with_invalid_data(self):
        # Remove the required 'name' field from project_data
        self.project_data.pop('name')

        # Get the create project url and post the data
        url = reverse('create_project')
        response = self.client.post(url, self.project_data)

        # Assert that the project was not created and the form is not valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 0)
        self.assertContains(response, 'This field is required.')
        
    def test_create_project_view_with_unauthorized_user(self):
        # Remove the user from the group to make them unauthorized
        self.group.user_set.remove(self.user)

        # Get the create project url and try to post the data
        url = reverse('create_project')
        response = self.client.post(url, self.project_data)

        # Assert that the user is unauthorized and cannot create a project
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.count(), 0)

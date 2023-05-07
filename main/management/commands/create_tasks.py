# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from main.models import Task, Project

# class Command(BaseCommand):
#     help = 'Creates pre-made tasks'

#     def handle(self, *args, **options):
#         projects = Project.objects.all()
#         tasks = [
            # {
            #     'title': 'Senior Project Proposal Draft',
            #     'description': 'Description for task 1',
            #     'project': projects[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the task
            # },
            # {
            #     'title': 'Final Report',
            #     'description': 'Description for task 2',
            #     'project': projects[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the task
            # },
#             # Add more tasks here
#         ]

#         for task in tasks:
#             t = Task(**task)
#             t.save()

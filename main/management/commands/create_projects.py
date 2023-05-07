# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from main.models import Project, Team

# class Command(BaseCommand):
#     help = 'Creates pre-made projects'

#     def handle(self, *args, **options):
#         teams = Team.objects.all()

#         projects = [
#             {
#                 'name': 'SDP 1',
#                 'description': 'Senior Development Project I',
#                 'start_date': timezone.now(),
#                 'end_date': timezone.now(),
#                 'status': 'Pending',
#                 'created_by': None,  # Set to the user who will create the project
#               },
#             {
#                 'name': 'SDP 2',
#                 'description': 'Senior Development Project II',
#                 'start_date': timezone.now(),
#                 'end_date': timezone.now(),
#                 'status': 'Pending',
#                 'created_by': None,  # Set to the user who will create the project
#              },
#             # Add more projects here
#         ]

#         for project in projects:
#             for team in teams:
#                 p = Project(**project)
#                 p.team = team
#                 p.save()

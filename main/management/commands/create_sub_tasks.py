# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from main.models import SubTask, Task

# class Command(BaseCommand):
#     help = 'Creates pre-made sub_tasks'

#     def handle(self, *args, **options):
#         tasks = Task.objects.all()
#         subtasks = [
            # {
            #     'title': 'Introduction',
            #     'description': 'Description of the problem.',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Project Objectives',
            #     'description': 'General and specific objectives',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'General Objectives',
            #     'description': 'General Objectives',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Specific Objectives',
            #     'description': 'Measureable objectives',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Related Works',
            #     'description': 'Description of similar solutions',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Preliminary Investigation',
            #     'description': 'Preliminary Investatgation',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Company Profile',
            #     'description': 'name of client, company or organization; address; line of business; company contact; list of stakeholder and their contact information',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Organizational Chart',
            #     'description': 'Chart of organization',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Statement of the Mission',
            #     'description': 'if any please write it down',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Project Request',
            #     'description': 'How the project was initiated',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Description of the Problem',
            #     'description': 'description of the problem to be investigated',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Project Scopes and Constraints',
            #     'description': 'Project Scopes and Constraints',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Expected Business Benefits',
            #     'description': 'Expected Business Benefits',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Expected System Benefits',
            #     'description': 'Expected System Benefits',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Planning',
            #     'description': 'Gantt chart',
            #     'task': tasks[0],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            
           


		    # {
            #     'title': 'Introduction',
            #     'description': 'Description of the problem',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Project Objectives',
            #     'description': 'General and specific objectives',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'General Objectives',
            #     'description': 'General Objectives',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Specific Objectives',
            #     'description': 'Measureable objectives',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Related Works',
            #     'description': 'Description of similar solutions',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Preliminary Investigation',
            #     'description': 'Preliminary Investatgation',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Company Profile',
            #     'description': 'name; address; line of business; company contact; stakeholder',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Organizational Chart',
            #     'description': 'Chart of organization',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Statement of the Mission',
            #     'description': 'if any please write it down',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Project Request',
            #     'description': 'How the project was initiated',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Description of the Problem',
            #     'description': 'description of the problem to be investigated',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Project Scopes and Constraints',
            #     'description': 'Project Scopes and Constraints',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Expected Business Benefits',
            #     'description': 'Expected Business Benefits',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Development Environment',
            #     'description': 'Details of the methodology, model, languages',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Feasibility Study',
            #     'description': 'Feasibility Study',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Technical Feasibility',
            #     'description': 'Technical Feasibility',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Legal Feasibility',
            #     'description': 'Legal Feasibility',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Operational Feasibility',
            #     'description': 'Operational Feasibility',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Schedule Feasibility',
            #     'description': 'ref.toAppendix-Software Cost Estimation',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Financial Feasibility',
            #     'description': 'ref.toAppendix-Software Cost Estimation',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            # {
            #     'title': 'Planning',
            #     'description': 'Gantt chart',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Analysis and Design',
            #     'description': 'Analysis and Design',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': "Design's Introduction",
            #     'description': "Design's Introduction",
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Risk Analysis',
            #     'description': 'spiral ref.Appendix -Software Cost Estimation',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Conduct of Analysis',
            #     'description': 'analysis method',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'User Requirements',
            #     'description': 'output Requirements',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
            #  {
            #     'title': 'Infrastructure Analysis',
            #     'description': 'Infrastructure Analysis',
            #     'task': tasks[1],
            #     'start_date': timezone.now(),
            #     'end_date': timezone.now(),
            #     'created_by': None,  # Set to the user who will create the subtask
            # },
           
            
            
            
			
            
#             # Add more subtasks here
#         ]

#         for subtask in subtasks:
#             s = SubTask(**subtask)
#             s.save()

# Generated by Django 4.2 on 2023-04-27 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0015_task_percent_complete_alter_task_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtask',
            name='assignee',
        ),
        migrations.AddField(
            model_name='subtask',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_sub_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]

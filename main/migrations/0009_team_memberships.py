# Generated by Django 4.2 on 2023-04-27 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_task_created_by_alter_project_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='memberships',
            field=models.ManyToManyField(blank=True, related_name='teams', to='main.membership'),
        ),
    ]

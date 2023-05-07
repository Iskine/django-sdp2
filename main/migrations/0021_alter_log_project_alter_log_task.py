# Generated by Django 4.2 on 2023-05-02 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_log_project_alter_log_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='project',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='main.project'),
        ),
        migrations.AlterField(
            model_name='log',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='main.task'),
        ),
    ]

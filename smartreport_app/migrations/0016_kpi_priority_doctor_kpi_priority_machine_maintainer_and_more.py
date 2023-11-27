# Generated by Django 4.2.7 on 2023-11-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0015_archivedreport_template_alter_archivedreport_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='priority_doctor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kpi',
            name='priority_machine_maintainer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kpi',
            name='priority_parent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kpi',
            name='priority_project_manager',
            field=models.IntegerField(default=0),
        ),
    ]

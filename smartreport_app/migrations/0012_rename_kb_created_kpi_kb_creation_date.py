# Generated by Django 4.2.7 on 2023-11-24 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0011_rename_created_kpi_kb_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kpi',
            old_name='kb_created',
            new_name='kb_creation_date',
        ),
    ]

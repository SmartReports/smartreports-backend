# Generated by Django 4.2.7 on 2023-11-24 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0009_rename_kb_id_kpi_kb_uid_remove_kpi_kb_source_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kpi',
            name='isNew',
        ),
    ]
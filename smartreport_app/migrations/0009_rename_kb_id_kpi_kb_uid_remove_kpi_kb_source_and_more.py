# Generated by Django 4.2.7 on 2023-11-24 15:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0008_merge_20231124_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kpi',
            old_name='kb_id',
            new_name='kb_uid',
        ),
        migrations.RemoveField(
            model_name='kpi',
            name='kb_source',
        ),
        migrations.AddField(
            model_name='kpi',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kpi',
            name='kb_frequency',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='kpi',
            name='kb_range',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='kpi',
            name='kb_taxonomy',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='reporttemplate',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

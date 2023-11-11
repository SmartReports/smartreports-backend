# Generated by Django 4.2.7 on 2023-11-11 10:30

from django.db import migrations, models
import smartreport_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0003_alter_kpi_allowed_charts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='allowed_charts',
            field=models.JSONField(default=smartreport_app.models.DEFAULT_CHART_CHOICES),
        ),
    ]
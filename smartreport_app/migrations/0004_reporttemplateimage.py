# Generated by Django 4.2.7 on 2023-11-23 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0003_dashboardlayout_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTemplateImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('doctor', 'Doctor'), ('parent', 'Parent'), ('project_manager', 'Project Manager'), ('machine_maintainer', 'Machine Maintainer')], max_length=128)),
                ('img', models.TextField(null=True)),
                ('report_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartreport_app.reporttemplate')),
            ],
        ),
    ]

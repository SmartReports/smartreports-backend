# Generated by Django 4.2.7 on 2023-11-13 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0002_alter_dashboardlayout_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardlayout',
            name='display',
            field=models.CharField(choices=[('xxs', 'xxs'), ('xs', 'xs'), ('sm', 'sm'), ('md', 'md'), ('lg', 'lg')], default='lg', max_length=10),
            preserve_default=False,
        ),
    ]

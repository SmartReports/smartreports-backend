# Generated by Django 4.2.7 on 2023-11-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartreport_app', '0004_kpi_isnew'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='barPlot',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='kpi',
            name='doughnutPlot',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='kpi',
            name='linePlot',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='kpi',
            name='piePlot',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='kpi',
            name='radarPlot',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='kpireportelement',
            name='chart_type',
            field=models.CharField(blank=True, choices=[('line', 'Line'), ('bar', 'Bar'), ('pie', 'Pie'), ('radar', 'Radar'), ('doughnut', 'Doughnut')], max_length=10, null=True),
        ),
    ]
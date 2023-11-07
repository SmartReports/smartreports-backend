from django.db import models
from django.utils.translation import gettext_lazy as _


class ChartType(models.TextChoices):
    LINE = 'line', _('Line')
    BAR = 'bar', _('Bar')
    PIE = 'pie', _('Pie')
    RADAR = 'radar', _('Radar')
    DOUGHNUT = 'doughnut' , _('Doughnut')

class UserType(models.TextChoices):
    DOCTOR = 'doctor', _('Doctor')
    PARENT = 'parent', _('Parent')
    PROJECT_MANAGER = 'project_manager', _('Project Manager')
    MACHINE_MAINTAINER = 'machine_maintainer', _('Machine Maintainer')

class FrequencyType(models.TextChoices):
    DAILY = 'daily', _('Daily')
    WEEKLY = 'weekly', _('Weekly')
    MONTHLY = 'monthly', _('Monthly')
    YEARLY = 'yearly', _('Yearly')
    QUARTERLY = 'quarterly', _('Quarterly')

class Kpi(models.Model):
    # Assuming you have a Kpi model with at least a name field.
    name = models.CharField(max_length=255)

    priorityForDoctor = models.IntegerField(default=9999)
    priorityForParent = models.IntegerField(default=9999)
    priorityForProject_manager = models.IntegerField(default=9999)
    priorityForMachine_mantainer = models.IntegerField(default=9999)

    linePlot = models.BooleanField(default=True)
    barPlot = models.BooleanField(default=True)
    piePlot = models.BooleanField(default=True)
    radarPlot = models.BooleanField(default=True)
    doughnutPlot = models.BooleanField(default=True)

    isNew = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)
    
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
    )

    frequency = models.CharField(
        max_length=20,
        choices=FrequencyType.choices,
    )

    def __str__(self):
        return self.name

class ReportTemplatePage(models.Model):
    report_template = models.ForeignKey(
        ReportTemplate,
        related_name='pages',
        on_delete=models.CASCADE
    )
    LAYOUT_CHOICES = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('grid', 'Grid'),
    ]
    layout = models.CharField(
        max_length=10,
        choices=LAYOUT_CHOICES
    )

    def __str__(self):
        return f"{self.report_template.name} - {self.get_layout_display()}"

class KpiReportElement(models.Model):
    report_page = models.ForeignKey(
        ReportTemplatePage,
        related_name='elements',
        on_delete=models.CASCADE
    )
    kpi = models.ForeignKey(
        Kpi,
        on_delete=models.CASCADE
    )
    chart_type = models.CharField(
        max_length=10,
        choices=ChartType.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.report_page.report_template.name} - {self.kpi.name}"


class Alarm(models.Model):
    
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
    )
    
    kpi = models.ForeignKey(
        Kpi,
        on_delete=models.CASCADE
    )

    min_value = models.FloatField()
    max_value = models.FloatField()

    def __str__(self):
        return self.name
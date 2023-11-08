from django.db import models
from django.utils.translation import gettext_lazy as _


# class ArchivedReport(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     file = models.FileField(upload_to="reports/")

class UserType(models.TextChoices):
    DOCTOR = 'doctor', _('Doctor')
    PARENT = 'parent', _('Parent')
    PROJECT_MANAGER = 'project_manager', _('Project Manager')
    MACHINE_MAINTAINER = 'machine_maintainer', _('Machine Maintainer')


class Kpi(models.Model):
  
    name = models.CharField(max_length=255)

    priorityDoctor = models.IntegerField(default=0)
    priorityParent = models.IntegerField(default=0)
    priorityProjectManager = models.IntegerField(default=0)
    priorityMachineMaintainer = models.IntegerField(default=0)
    isNew = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ChartType(models.Model):

    kpi = models.ForeignKey(
        Kpi, 
        related_name="allowed_charts",
        on_delete=models.CASCADE
    )

    CHART_CHOICES = [
        ('line', 'Line'), 
        ('bar', 'Bar'),
        ('scatter', 'Scatter'),
        ('pie', 'Pie'),
    ]
    plot_name = models.CharField(max_length=128, choices=CHART_CHOICES)


class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)

    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("quarterly", "Quarterly"),
    ]
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    # Pages will be a reverse relation from ReportTemplatePage

    def __str__(self):
        return self.name


class ReportTemplatePage(models.Model):
    report_template = models.ForeignKey(
        ReportTemplate, related_name="pages", on_delete=models.CASCADE
    )
    LAYOUT_CHOICES = [
        ("horizontal", "Horizontal"),
        ("vertical", "Vertical"),
        ("grid", "Grid"),
    ]
    layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES)

    def __str__(self):
        return f"{self.report_template.name} - {self.get_layout_display()}"


class KpiReportElement(models.Model):
    report_page = models.ForeignKey(
        ReportTemplatePage, related_name="elements", on_delete=models.CASCADE
    )
    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE)
    chart_type = models.CharField(
        max_length=128,
    )

    def __str__(self):
        return f"{self.report_page.report_template.name} - {self.kpi.name}"
 

class Alarm(models.Model):
    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE)

    min_value = models.FloatField()
    max_value = models.FloatField()

    def __str__(self):
        return self.name

class DashboardLayout(models.Model):
    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    layout = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

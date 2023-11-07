from django.db import models
from django.utils.translation import gettext_lazy as _

class Kpi(models.Model):
    # Assuming you have a Kpi model with at least a name field.
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ChartType(models.TextChoices):
    LINE = 'line', _('Line')
    BAR = 'bar', _('Bar')
    PIE = 'pie', _('Pie')
    SCATTER = 'scatter', _('Scatter')

class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('quarterly', 'Quarterly'),
    ]
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES
    )
    # Pages will be a reverse relation from ReportTemplatePage

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
    # Elements will be a reverse relation from KpiReportElement

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

class User(models.Model):
    CATEGORY_CHOICES = [
        ('doctor', 'Doctor'),
        ('parent', 'Parent'),
        ('project_manager', 'Project_manager'),
        ('machine_mantainer', 'Machine_mantainer'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )
    email = models.EmailField()
    token = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class Alarm(models.Model):
    kpi = models.ForeignKey(
        Kpi,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='alarms',
        on_delete=models.CASCADE
    )
    min_value = models.FloatField()
    max_value = models.FloatField()

    def __str__(self):
        return self.name
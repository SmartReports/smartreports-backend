from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError


class UserType(models.TextChoices):
    DOCTOR = "doctor", _("Doctor")
    PARENT = "parent", _("Parent")
    PROJECT_MANAGER = "project_manager", _("Project Manager")
    MACHINE_MAINTAINER = "machine_maintainer", _("Machine Maintainer")


CHART_CHOICES = (
    "line",
    "bar",
    "pie",
    "doughnut",
    "radar",
)


def DEFAULT_CHART_CHOICES():
    return [*CHART_CHOICES]


class Kpi(models.Model):
    name = models.CharField(max_length=255)

    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    allowed_charts = models.JSONField(default=DEFAULT_CHART_CHOICES)

    priority = models.IntegerField(default=0)

    isNew = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not isinstance(self.allowed_charts, list):
            raise ValidationError("Allowed charts must be a list")
        for chart in self.allowed_charts:
            if chart not in CHART_CHOICES:
                raise ValidationError(f"{chart} is not a valid chart type")


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


class DashboardLayout(models.Model):
    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )
    
    DISPLAY_CHOICES = [
        ("xxs", "xxs"),
        ("xs", "xs"),
        ("sm", "sm"),
        ("md", "md"),
        ("lg", "lg"),
    ]
    
    display = models.CharField(max_length=10, choices=DISPLAY_CHOICES)

    layout = models.JSONField()


class ArchivedReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    sent = models.BooleanField(default=False)

    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    template = models.ForeignKey(
        ReportTemplate, related_name="archived_reports", on_delete=models.CASCADE
    )

    file = models.FileField(upload_to="reports/")


class Email(models.Model):
    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    emails = models.JSONField()

    def clean(self):
        if not isinstance(self.emails, list):
            raise ValidationError("Emails must be a list")

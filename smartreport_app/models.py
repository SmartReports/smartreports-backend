from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django_storage_supabase import SupabaseStorage


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

USER_CHOICES = (
    "doctor",
    "parent",
    "project_manager",
    "machine_maintainer",
)
def DEFAULT_USER_CHOICES():
    return [*USER_CHOICES]



class Kpi(models.Model):

    # field from the kb
    kb_uid = models.CharField(max_length=255)
    kb_name = models.CharField(max_length=255)
    kb_description = models.TextField(blank=True)
    kb_taxonomy = models.TextField(blank=True)
    kb_range = models.CharField(max_length=255, blank=True)
    kb_formula = models.TextField(blank=True)
    kb_unit = models.CharField(max_length=255, blank=True)
    kb_frequency = models.CharField(max_length=255, blank=True)
    kb_creation_date = models.DateTimeField(blank=True)
    kb_counter = models.IntegerField(default=0)

    # internal field
    user_type = models.JSONField(default=DEFAULT_USER_CHOICES, blank=True, null=True)
    priority_doctor = models.IntegerField(default=0)
    priority_parent = models.IntegerField(default=0)
    priority_project_manager = models.IntegerField(default=0)
    priority_machine_maintainer = models.IntegerField(default=0)
    allowed_charts = models.JSONField(default=DEFAULT_CHART_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.kb_name

    priority = models.IntegerField(default=0)


    def __str__(self):
        return self.kb_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not isinstance(self.allowed_charts, list):
            raise ValidationError("Allowed charts must be a list")
        for chart in self.allowed_charts:
            if chart not in CHART_CHOICES:
                raise ValidationError(f"{chart} is not a valid chart type")
        
        if not isinstance(self.user_type, list):
            raise ValidationError("User type must be a list")
        for user in self.user_type:
            if user not in USER_CHOICES:
                raise ValidationError(f"{user} is not a valid user type")


class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)

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
class ReportTemplateImage(models.Model):
    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )
    report_id = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    img = models.TextField(null=True)

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

    kpis = models.ManyToManyField(Kpi)

    chart_type = models.CharField(
        max_length=128,
    )


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

    file = models.TextField(null=True)
    file_name = models.TextField(null=True)


class Email(models.Model):
    user_type = models.CharField(
        max_length=128,
        choices=UserType.choices,
    )

    emails = models.JSONField()

    def clean(self):
        if not isinstance(self.emails, list):
            raise ValidationError("Emails must be a list")

from django.contrib import admin
from .models import (
    Kpi,
    ReportTemplate,
    ReportTemplatePage,
    KpiReportElement,
    Alarm,
    DashboardLayout
)


class KpiReportElementInline(admin.TabularInline):
    model = KpiReportElement
    extra = 1


class ReportTemplatePageInline(admin.TabularInline):
    model = ReportTemplatePage
    extra = 1
    show_change_link = True
    inlines = [KpiReportElementInline]


@admin.register(Kpi)
class KpiAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "frequency")
    list_filter = ("frequency",)
    inlines = [ReportTemplatePageInline]


@admin.register(ReportTemplatePage)
class ReportTemplatePageAdmin(admin.ModelAdmin):
    list_display = ("report_template", "layout")
    list_filter = ("layout",)
    inlines = [KpiReportElementInline]


@admin.register(KpiReportElement)
class KpiReportElementAdmin(admin.ModelAdmin):
    list_display = ("report_page", "kpi", "chart_type")
    list_filter = ("chart_type",)


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ("id", "user_type", "kpi", "min_value", "max_value")
    list_filter = ("user_type", "kpi")
    search_fields = ("user_type", "kpi__name")

    def get_kpi_name(self, obj):
        return obj.kpi.name

    get_kpi_name.short_description = "KPI Name"

@admin.register(DashboardLayout)
class DashboardLayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'layout')  # Fields to display in the list view
    list_filter = ("user_type", )
    search_fields = ('user_type',)  # Fields to enable searching in the admin interface

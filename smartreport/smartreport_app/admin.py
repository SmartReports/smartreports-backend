from django.contrib import admin
from .models import Kpi, ReportTemplate, ReportTemplatePage, KpiReportElement

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
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency')
    list_filter = ('frequency',)
    inlines = [ReportTemplatePageInline]

@admin.register(ReportTemplatePage)
class ReportTemplatePageAdmin(admin.ModelAdmin):
    list_display = ('report_template', 'layout')
    list_filter = ('layout',)
    inlines = [KpiReportElementInline]

@admin.register(KpiReportElement)
class KpiReportElementAdmin(admin.ModelAdmin):
    list_display = ('report_page', 'kpi', 'chart_type')
    list_filter = ('chart_type',)
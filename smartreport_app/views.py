from django.shortcuts import render
from .models import KpiReportElement, ReportTemplatePage, ReportTemplate, Kpi, Alarm, ChartType, DashboardLayout
from .serializers import ReportTemplatePageSerializer, ReportTemplateSerializer, KpiReportElementSerializer, KpiSerializer, AlarmSerializer, ChartTypeSerializer, DashboardLayoutSerializer

from rest_framework import viewsets

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer

class ReportTemplatePageViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplatePage.objects.all()
    serializer_class = ReportTemplatePageSerializer

class KpiReportElementViewSet(viewsets.ModelViewSet):
    queryset = KpiReportElement.objects.all()
    serializer_class = KpiReportElementSerializer

class KpiViewSet(viewsets.ModelViewSet):
    queryset = Kpi.objects.all()
    serializer_class = KpiSerializer

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

class ChartTypeViewSet(viewsets.ModelViewSet):
    queryset = ChartType.objects.all()
    serializer_class = ChartTypeSerializer

class DashboardLayoutViewSet(viewsets.ModelViewSet):
    queryset = DashboardLayout.objects.all()
    serializer_class = DashboardLayoutSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        param_value = self.request.query_params.get('user_type', None)
        if param_value is not None:
            queryset = queryset.filter(your_field=param_value)
        return queryset
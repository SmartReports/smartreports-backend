from django.shortcuts import render
from .models import KpiReportElement, ReportTemplatePage, ReportTemplate, Kpi, Alarm, ChartType, DashboardLayout
from .serializers import ReportTemplatePageSerializer, ReportTemplateSerializer, KpiReportElementSerializer, KpiSerializer, AlarmSerializer, ChartTypeSerializer, DashboardLayoutSerializer

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'user_type' ]    

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'user_type' ]

class ChartTypeViewSet(viewsets.ModelViewSet):
    queryset = ChartType.objects.all()
    serializer_class = ChartTypeSerializer

class DashboardLayoutViewSet(viewsets.ModelViewSet):
    queryset = DashboardLayout.objects.all()
    serializer_class = DashboardLayoutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'user_type' ]
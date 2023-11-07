from django.shortcuts import render
from .models import KpiReportElement, ReportTemplatePage, ReportTemplate
from .serializers import ReportTemplatePageSerializer, ReportTemplateSerializer, KpiReportElementSerializer

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

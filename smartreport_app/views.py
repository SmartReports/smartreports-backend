import os
from typing import Any
import django_filters
from .sync_db_kb import sync_kpi_lits
from .email import send_emails_for_unsent_reports

from .models import (
    KpiReportElement,
    ReportTemplatePage,
    ReportTemplate,
    ReportTemplateImage,
    Kpi,
    Alarm,
    DashboardLayout,
    ArchivedReport,
    SmartReportTemplate,
)
from .serializers import (
    ReportTemplatePageSerializer,
    ReportTemplateSerializer,
    ReportTemplateImageSerializer,
    KpiReportElementSerializer,
    KpiSerializer,
    AlarmSerializer,
    DashboardLayoutSerializer,
    ArchivedReportSerializer,
    SmartTemplateSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .kb_interface import kb_interface

class SmartReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = SmartReportTemplate.objects.filter(smart=True)
    serializer_class = SmartTemplateSerializer
    filterset_fields = ["user_type"]

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.filter(smart=False)
    serializer_class = ReportTemplateSerializer
    filterset_fields = ["user_type"]

class ReportTemplatePageViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplatePage.objects.all()
    serializer_class = ReportTemplatePageSerializer

class ReportTemplateImageViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplateImage.objects.all()
    serializer_class = ReportTemplateImageSerializer
    filterset_fields = ["user_type", "report_id"]

class KpiReportElementViewSet(viewsets.ModelViewSet):
    queryset = KpiReportElement.objects.all()
    serializer_class = KpiReportElementSerializer


class KpiFilter(django_filters.FilterSet):
    user_type = django_filters.CharFilter(method='filter_user_type')

    class Meta:
        model = Kpi
        fields = ['user_type']

    def filter_user_type(self, queryset, name, value):
        # Access the value from the GET query parameters
        user_type_value = self.request.query_params.get('user_type')

        print(user_type_value)
        # Check if the value is provided
        if user_type_value: 
            filtered_queryset = []
            for kpi_instance in queryset:
                print(kpi_instance.user_type)
                if user_type_value in kpi_instance.user_type:
                    filtered_queryset.append(kpi_instance.pk)
            return Kpi.objects.filter(id__in=filtered_queryset)
        else:
            return queryset
    

class KpiViewSet(viewsets.ModelViewSet):
    queryset = Kpi.objects.all()
    serializer_class = KpiSerializer
    filterset_class = KpiFilter

    def list(self, request, *args, **kwargs):

        # sync_kpi_lits()

        return super().list(request, *args, **kwargs)


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    filterset_fields = ["user_type"]


class DashboardLayoutViewSet(viewsets.ModelViewSet):
    queryset = DashboardLayout.objects.all()
    serializer_class = DashboardLayoutSerializer
    filterset_fields = ["user_type", "display"]

class KpiDataViewSet(viewsets.GenericViewSet):
    def __init__(self, **kwargs: Any) -> None:
        if (os.environ.get("DEBUG").lower() == "false"):
            self.permission_classes = [IsAuthenticated]
        super().__init__(**kwargs)

    def list(self, request):
        params = request.query_params
        list_of_internal_ids = params.getlist("kpis")[0].split(',') # list of kpis to show in the plot
        
        queryset = Kpi.objects.filter(id__in=list_of_internal_ids)
        
        # translate in a list of ids for the KB
        list_of_KB_uids = list(queryset.values_list("kb_uid", flat=True))

        if 'chart_type' not in params:
            return Response({"message": "The required parameter 'chart_type' is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        if list_of_KB_uids == []:
            return Response({"message": "No kpis found"}, status=status.HTTP_400_BAD_REQUEST)
        
        for kpi in Kpi.objects.filter(id__in=list_of_internal_ids):
            if not params["chart_type"] in kpi.allowed_charts:
                return Response({"message": f"Kpi {kpi.pk} does not support {params['chart_type']} plot"}, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO implement start and end time
        kb_interface_params = {
            'chart_type' : params['chart_type'],
            'kpi_KB_uid_list' : list_of_KB_uids,
            'kpi_frequency_list' : [kpi.kb_frequency in queryset],
            'start_time' : 'boh',
            'end_time' : 'boh', 
        }
        
        data = kb_interface(params = kb_interface_params)
        return Response({"data": data})


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = ArchivedReport.objects.all()
    serializer_class = ArchivedReportSerializer
    filterset_fields = ["user_type"]


class SyncKBViewSet(viewsets.GenericViewSet):
    def __init__(self, **kwargs: Any) -> None:
        if (os.environ.get("DEBUG").lower() == "false"):
            self.permission_classes = [IsAuthenticated]
        super().__init__(**kwargs)
    
    def list(self, request):
        sync_kpi_lits()
        return Response({"message": "Syncing KB"})


class SendEmailsViewSet(viewsets.GenericViewSet):
    def __init__(self, **kwargs: Any) -> None:
        if (os.environ.get("DEBUG").lower() == "false"):
            self.permission_classes = [IsAuthenticated]
        super().__init__(**kwargs)
    
    def list(self, request):
        send_emails_for_unsent_reports()
        return Response({"message": "Sending emails"})
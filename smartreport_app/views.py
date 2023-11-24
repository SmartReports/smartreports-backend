import os
from typing import Any
import django_filters
from .sync_db_kb import sync_kpi_lits

from .models import (
    KpiReportElement,
    ReportTemplatePage,
    ReportTemplate,
    Kpi,
    Alarm,
    DashboardLayout,
    ArchivedReport,
)
from .serializers import (
    ReportTemplatePageSerializer,
    ReportTemplateSerializer,
    KpiReportElementSerializer,
    KpiSerializer,
    AlarmSerializer,
    DashboardLayoutSerializer,
    ArchivedReportSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .kb_interface import kb_interface


class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    filterset_fields = ["user_type"]

class ReportTemplatePageViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplatePage.objects.all()
    serializer_class = ReportTemplatePageSerializer


class KpiReportElementViewSet(viewsets.ModelViewSet):
    queryset = KpiReportElement.objects.all()
    serializer_class = KpiReportElementSerializer

# TODO CHECK
class KpiFilter(django_filters.FilterSet):
    user_type = django_filters.CharFilter(method='filter_user_type')

    class Meta:
        model = Kpi
        fields = ['user_type']

    def filter_user_type(self, queryset, name, value):
        # Access the value from the GET query parameters
        user_type_value = self.request.query_params.get('user_type')

        # Check if the value is provided
        if user_type_value: # TODO fix
            filtered_queryset = []
            for kpi_instance in queryset:
                if user_type_value in kpi_instance.user_type:
                    filtered_queryset.append(kpi_instance)
            return filtered_queryset
        else:
            return queryset
    
# TODO CHECK
class KpiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kpi.objects.all()
    serializer_class = KpiSerializer
    filterset_class = KpiFilter

    def list(self, request, *args, **kwargs):
        # external function 
        sync_kpi_lits()

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
        print(type(Kpi.objects.all().get(pk=1)))
        return Response({"message": "This endpoint is not available"})
    
    def retrieve(self, request, pk=None):
        if pk == None:
            return Response({"message": "How the f**k did you get here?"})
        kpi_name = Kpi.objects.get(pk=pk).name
        params = request.query_params
        if 'chart_type' not in params:
            return Response({"message": "The required parameter 'chart_type' is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if False:  # enable in production
            # check if the required kpi exists
            if not Kpi.objects.filter(
                name=params["kpi_name"], user_type=params["user_type"]
            ).exists():
                return Response(
                    {"message": "The requested kpi does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # check if the required chart type is supported for the required kpi
            if not Kpi.objects.filter(
                name=params["kpi_name"],
                user_type=params["user_type"],
                allowed_charts__plot_name=params["chart_type"],
            ).exists():
                return Response(
                    {
                        "message": "The requested chart type is not supported for the requested kpi"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        data = kb_interface(kpi_name, params)
        return Response({"data": data})


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = ArchivedReport.objects.all()
    serializer_class = ArchivedReportSerializer
    filterset_fields = ["user_type"]
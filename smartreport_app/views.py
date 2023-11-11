from django.shortcuts import render
from .models import (
    KpiReportElement,
    ReportTemplatePage,
    ReportTemplate,
    Kpi,
    Alarm,
    DashboardLayout,
)
from .serializers import (
    ReportTemplatePageSerializer,
    ReportTemplateSerializer,
    KpiReportElementSerializer,
    KpiSerializer,
    AlarmSerializer,
    DashboardLayoutSerializer,
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


class KpiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kpi.objects.all()
    serializer_class = KpiSerializer
    filterset_fields = ["user_type", "name"]


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    filterset_fields = ["user_type"]


class DashboardLayoutViewSet(viewsets.ModelViewSet):
    queryset = DashboardLayout.objects.all()
    serializer_class = DashboardLayoutSerializer
    filterset_fields = ["user_type"]

class KpiDataViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
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
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


@api_view(["GET"])
def kpi_data(request, format=None):
    if not request.method == "GET":
        return Response(
            {f"message": "{request.method} method is not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    params = request.query_params

    # check if the parameters "kpi_name" and "user_type" are provided
    if (
        not "kpi_id" in params
        or not "user_type" in params
        or not "chart_type" in params
    ):
        return Response(
            {
                "message": "The required parameters 'kpi_name' and 'user_type' are missing"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    kpi_name = Kpi.objects.get(pk=params["kpi_id"]).name

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

    # ask the kb for the response, the format is different depending on the kind of plot

    data = kb_interface(kpi_name, params)

    return Response({"data": data})

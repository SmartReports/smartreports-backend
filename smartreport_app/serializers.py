from rest_framework import serializers
from .models import KpiReportElement, ReportTemplatePage, ReportTemplate, Kpi, Alarm, ChartType, DashboardLayout


class KpiReportElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KpiReportElement
        fields = "__all__"


class ReportTemplatePageSerializer(serializers.ModelSerializer):
    elements = KpiReportElementSerializer(many=True)

    class Meta:
        model = ReportTemplatePage
        fields = "__all__"


class ReportTemplateSerializer(serializers.ModelSerializer):
    pages = ReportTemplatePageSerializer(many=True)

    class Meta:
        model = ReportTemplate
        fields = "__all__"

    def create(self, validated_data):
        # Extract pages data from the validated data.
        pages_data = validated_data.pop("pages")

        # Create the report template instance.
        report_template = ReportTemplate.objects.create(**validated_data)

        # Create report template pages and elements.
        for page_data in pages_data:
            elements_data = page_data.pop("elements")
            # Create report template page instance.
            report_page = ReportTemplatePage.objects.create(
                report_template=report_template, **page_data
            )

            # Create each KPI report element for the page.
            for element_data in elements_data:
                KpiReportElement.objects.create(report_page=report_page, **element_data)

        return report_template
    
class ChartTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartType
        fields = "__all__"


class KpiSerializer(serializers.ModelSerializer):
    allowed_charts = ChartTypeSerializer(many=True, required=False)
    
    class Meta:
        model = Kpi
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['allowed_charts'] = [chart['plot_name'] for chart in data['allowed_charts']]
        return data


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = "__all__"

class DashboardLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardLayout
        fields = "__all__"
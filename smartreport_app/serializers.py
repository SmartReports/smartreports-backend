from rest_framework import serializers
from .models import KpiReportElement, ReportTemplatePage, ReportTemplate, Kpi, User, Alarm

class KpiReportElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KpiReportElement
        fields = ['kpi', 'chart_type']

class ReportTemplatePageSerializer(serializers.ModelSerializer):
    elements = KpiReportElementSerializer(many=True)

    class Meta:
        model = ReportTemplatePage
        fields = ['layout', 'elements']

class ReportTemplateSerializer(serializers.ModelSerializer):
    pages = ReportTemplatePageSerializer(many=True)

    class Meta:
        model = ReportTemplate
        fields = '__all__'

    def create(self, validated_data):
        # Extract pages data from the validated data.
        pages_data = validated_data.pop('pages')
        
        # Create the report template instance.
        report_template = ReportTemplate.objects.create(**validated_data)
        
        # Create report template pages and elements.
        for page_data in pages_data:
            elements_data = page_data.pop('elements')
            # Create report template page instance.
            report_page = ReportTemplatePage.objects.create(report_template=report_template, **page_data)
            
            # Create each KPI report element for the page.
            for element_data in elements_data:
                KpiReportElement.objects.create(report_page=report_page, **element_data)
        
        return report_template


class KpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kpi
        fields = '__all__'
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'
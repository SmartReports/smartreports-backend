from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'report-templates', views.ReportTemplateViewSet)
router.register(r'report-template-pages', views.ReportTemplatePageViewSet)
router.register(r'kpi-report-elements', views.KpiReportElementViewSet)
router.register(r'kpi-list', views.KpiViewSet)
router.register(r'alarms-list', views.AlarmViewSet)
router.register(r'chart-types', views.ChartTypeViewSet)
router.register(r'dashboard-layout', views.DashboardLayoutViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('kpi-data/', views.kpi_data)
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"report-templates", views.ReportTemplateViewSet)
router.register(r"report-template-pages", views.ReportTemplatePageViewSet)
router.register(r"kpi-report-elements", views.KpiReportElementViewSet)
router.register(r"kpi-list", views.KpiViewSet)
router.register(r"alarms-list", views.AlarmViewSet)
router.register(r"report-img", views.ReportTemplateImageViewSet)
router.register(r"dashboard-layout", views.DashboardLayoutViewSet)
router.register(r"report-archive", views.ArchivedReportViewSet)
router.register(r"kpi-data", views.KpiDataViewSet, basename="kpi-data")
router.register(r'sync-kb', views.SyncKBViewSet, basename='sync-kb')
router.register(r'send-reports', views.SendReportEmailsViewSet, basename='send-emails')
router.register(r'send-alarms', views.SendAlarmEmailsViewSet, basename='send-alarms')

# The API URLs are now determined automatically by the router.
urlpatterns = [path("", include(router.urls))]

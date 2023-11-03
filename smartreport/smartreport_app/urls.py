from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'report-templates', views.ReportTemplateViewSet)
router.register(r'report-template-pages', views.ReportTemplatePageViewSet)
router.register(r'kpi-report-elements', views.KpiReportElementViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
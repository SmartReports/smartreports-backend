

from smartreport_app.models import DashboardLayout, Kpi

def compute_orderings():
    dashboards = DashboardLayout.objects.all()
    for d in dashboards:
        print(d)
    kpis = Kpi.objects.all()
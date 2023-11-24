import requests
from .models import Kpi


URL = 'https://vornao.dev:8888/kpis'
USERNAME = 'smartapp'
PASSWORD = 'api'


def sync_kpi_lits():

    print("start sync_kpi_lits")

    kpi_list = requests.get(URL, auth=(USERNAME, PASSWORD))

    for kpi in kpi_list.json()['data']:

        # if we don't have this kpi in our db, create it

        if Kpi.objects.filter(kb_id=kpi['kpi_id']).exists():
            continue
        
        kpi_instance = Kpi(
            kb_name = kpi['name'],
            kb_id = kpi['kpi_id'],
            kb_description = kpi['description'],
            kb_formula = kpi['formula'],
            kb_unit = kpi['unit'],
            kb_source = kpi['source'],
            kb_counter = kpi['counter'],
            user_type=[],
            allowed_charts=[],
            priority=0,
            isNew=True
        )
        kpi_instance.save()
        print(f"KPI {kpi['kpi_id']} created")

    
if __name__ == '__main__':
    sync_kpi_lits()
    print('KPIs synced')
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

        if Kpi.objects.filter(kb_uid=kpi['uid']).exists():
            # update the counter
            kpi_instance = Kpi.objects.get(kb_uid=kpi['uid'])
            kpi_instance.kb_name = kpi['name']
            kpi_instance.kb_description = kpi['description']
            kpi_instance.kb_taxonomy = kpi['taxonomy']
            kpi_instance.kb_range = kpi['kpi_range']
            kpi_instance.kb_formula = kpi['formula']
            kpi_instance.kb_unit = kpi['unit']
            kpi_instance.kb_frequency = kpi['frequency']
            kpi_instance.kb_creation_date = kpi['creation_date']
            kpi_instance.kb_counter = kpi['counter']

            kpi_instance.save()
            print(f"KPI {kpi['uid']} updated")
        
        else:
    
            kpi_instance = Kpi(
                
                kb_uid = kpi['uid'],
                kb_name = kpi['name'],
                kb_description = kpi['description'],
                kb_taxonomy = kpi['taxonomy'],
                kb_range = kpi['kpi_range'],
                kb_formula = kpi['formula'],
                kb_unit = kpi['unit'],
                kb_frequency = kpi['frequency'],
                kb_creation_date = kpi['creation_date'],
                kb_counter = kpi['counter'],
            )
            kpi_instance.save()
            print(f"KPI {kpi['uid']} created")

    
if __name__ == '__main__':
    sync_kpi_lits()
    print('KPIs synced')
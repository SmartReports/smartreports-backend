import requests
from .models import Kpi
import random


BASE_URL = 'https://vornao.dev:8888'
USERNAME = 'smartapp'
PASSWORD = 'api'


def sync_kpi_lits():

    url = BASE_URL+'/kpis'

    print(f"start sync_kpi_lits, URL={url}")

    kpi_list = requests.get(url, auth=(USERNAME, PASSWORD))

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


def get_kpi_value(kpi_uid, start_time=0, end_time=0):
    # kpi_value = requests.get(f'{BASE_URL}/kpi/{kpi_uid}', auth=(USERNAME, PASSWORD))
    # return kpi_value.json()['data']
    
    # TODO random values for a weekly kpi
    kpi_value = {
        'data' : {
            'name' : kpi_uid,
            'value' : [random.random() for _ in range(7)]
        }
    }

    return kpi_value['data']
    
    
    
if __name__ == '__main__':
    sync_kpi_lits()
    print('KPIs synced')
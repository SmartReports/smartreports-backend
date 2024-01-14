import requests
from .models import Kpi
import random
import pandas as pd

BASE_URL = 'https://industrial-smartapp-api.onrender.com'
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

    name = Kpi.objects.get(kb_uid=kpi_uid).kb_name
    
    if kpi_uid.startswith('all'): # kpi di simone
        df = pd.read_csv('./kb_daily.csv')
        kpi_value = {
            'data' : {
                'name' : name,
                'value' : df[kpi_uid].tolist()
            }
        }

        return kpi_value['data']

    else:   # kpi random belline
        kpi_value = {
            'data' : {
                'name' : name,
                'value' : [random.random() for _ in range(7)]
            }
        }

        return kpi_value['data']

        
if __name__ == '__main__':
    sync_kpi_lits()
    print('KPIs synced')
import requests
from .models import Kpi
import random
import copy

BASE_URL = 'https://industrial-smartapp-api.onrender.com'
USERNAME = 'smartapp'
PASSWORD = 'api'

simo_kpi = {
  "date": ["2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15"],
  "all_machines_availability": [0.7093253968253967, 0.6359126984126984, 0.6374007936507936, 0.7324735449735449, 0.5219907407407407, 0.6121031746031745, 0.5714285714285714],
  "all_machines_performance": [0.9592240686301553, 0.9717855976569765, 0.9830589750706683, 0.9740554062976611, 0.9911840078009655, 0.9892214809701199, 0.9833326159377656],
  "all_machines_quality": [0.9068031656200728, 0.9238238465119826, 0.8923965444411264, 0.9520257594506903, 0.8646438066039629, 0.7768992808312886, 0.7696293751514001],
  "all_machines_oee": [0.5885732338353517, 0.5384252039315043, 0.5248256921527835, 0.6622691770019036, 0.39944311659722864, 0.38456645072490664, 0.3342573982228372]
}


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

    simo_kpi_copy = copy.deepcopy(simo_kpi)
    
    if kpi_uid.startswith('all'): # kpi di simone
        kpi_value = {
            'data' : {
                'name' : name,
                'value' : simo_kpi_copy[kpi_uid]
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
from .sync_db_kb import get_kpi_value
import random


def kb_interface(params):
    plot_type = params['chart_type']
    kpi_list = params['kpi_KB_uid_list'] # id of the kpi in the kb
    start_time = params['start_time']
    end_time = params['end_time']
    frequency = params['kpi_frequency_list']

    if plot_type == 'semaphore':
        resp = get_kpi_value(kpi_list[0]) # is only one
        value = resp['value'][-1]
        response = {
            'value': value,  # should be only one or take the last one
            'color' : random.choice(['red', 'orange', 'green'])
        }
        return response
    
    if plot_type == 'value':
        resp = get_kpi_value(kpi_list[0]) # is only one
        value = resp['value'][-1]
        response = {
            'value': value,  # should be only one or take the last one
        }
        return response


    colors = [
        'rgb(54, 162, 235)',
        'rgb(255, 98, 132)',
        'rgb(75, 193, 193)',
        'rgb(255, 159, 64)',
        'rgb(154, 102, 255)',
        'rgb(255, 205, 86)',
        'rgb(201, 203, 208)'
    ]
    transp_colors = [color[:-1]+', 0.2)' for color in colors]
    frequencies_lbls = {
        'monthly': [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ],
        'hourly': [str(i)+':00' for i in range(24)],
        'daily': [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]
    }

    if frequency == 'monthly':
        start_freq = start_time.month # int in [0,11]
    elif frequency == 'daily':
        start_freq = start_time.day # int in [0,6]
    elif frequency == 'hourly':
        start_freq = start_time.hour # int in [0,11]
    elif frequency == 'weekly':
        start_freq = 0


    kb_resps = []
    for i, kpi_uid in enumerate(kpi_list):
        kn_resp = get_kpi_value(kpi_uid, start_time, end_time) # call to group 1 api
        kb_resps.append(kn_resp)

    frequencies_lbls['weekly'] = [f'Week {i}' for i in range(len(kb_resps[0]['value']))] # assuming they all have the same length

    labels = []
    datasets = []
    for i in range(len(kb_resps[0]['value'])): # assuming they all have the same length
        labels.append(frequencies_lbls[frequency][(i+start_freq)%len(frequencies_lbls[frequency])])
    for i, kb_resp in enumerate(kb_resps):
        dataset = {}
        dataset['label'] = kb_resp['name']
        dataset['data'] = kb_resp['value']
        if plot_type == 'line':
            dataset['fill'] = False
            dataset['borderColor'] = colors[i%len(colors)]
            dataset['backgroundColor'] = transp_colors[i%len(colors)]
            dataset['tension'] = 0.1
        elif plot_type == 'bar':
            dataset['borderColor'] = colors[i%len(colors)]
            dataset['backgroundColor'] = colors[i%len(colors)]
            dataset['borderWidth'] = 1
        elif plot_type=='radar':
            dataset['fill'] = True
            dataset['borderColor'] = colors[i%len(colors)]
            dataset['backgroundColor'] = transp_colors[i%len(colors)]
        elif plot_type == 'pie' or plot_type == 'doughnut':
            dataset['backgroundColor'] = colors
        datasets.append(dataset)

    response = {
        'labels': labels,
        'datasets': datasets
    }

    return response
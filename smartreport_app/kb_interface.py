from .sync_db_kb import get_kpi_value
import numpy as np

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
            'value': value,  # should be only only one or take the last one
            'color' : np.random.choice(['red', 'orange', 'green'])
        }
        return response


    colors = [
        'rgb(0.4, 0.7607843137254902, 0.6470588235294118)',
        'rgb(0.9882352941176471, 0.5529411764705883, 0.3843137254901961)',
        'rgb(0.5529411764705883, 0.6274509803921569, 0.796078431372549)',
        'rgb(0.9058823529411765, 0.5411764705882353, 0.7647058823529411)',
        'rgb(0.6509803921568628, 0.8470588235294118, 0.32941176470588235)',
        'rgb(1.0, 0.8509803921568627, 0.1843137254901961)',
        'rgb(0.8980392156862745, 0.7686274509803922, 0.5803921568627451)',
        'rgb(0.7019607843137254, 0.7019607843137254, 0.7019607843137254)'
    ]
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
        'hourly': [str(i) for i in range(24)],
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
        kn_resp = get_kpi_value(kpi_uid, start_time, end_time ) # call to group 1 api
        kb_resps.append(kn_resp)

    frequencies_lbls['weekly'] = [f'Week {i}' for i in range(len(kb_resps[0]['value']))] # assuming they all have the same length

    labels = []
    datasets = []
    if plot_type == 'radar':
        for kb_resp in kb_resps:
            labels.append(kb_resp['name'])
        for i in range(len(kb_resps[0]['value'])): # assuming they all have the same length
            dataset = {}
            dataset['label'] = frequencies_lbls[frequency][(i+start_freq)%len(frequencies_lbls[frequency])]
            dataset['data'] = [kb_resp['value'][i] for kb_resp in kb_resps]
            dataset['fill'] = True
            dataset['backgroundColor'] = colors[i%len(colors)]
            dataset['pointBackgroundColor'] = colors[i%len(colors)]
            dataset['pointBorderColor'] = '#fff'
            dataset['pointHoverBackgroundColor'] = '#fff'
            dataset['pointHoverBorderColor'] = colors[i%len(colors)]
            datasets.append(dataset)
    else:
        for i in range(len(kb_resps[0]['value'])): # assuming they all have the same length
            labels.append(frequencies_lbls[frequency][(i+start_freq)%len(frequencies_lbls[frequency])])
        for i, kb_resp in enumerate(kb_resps):
            dataset = {}
            if plot_type == 'line':
                dataset['label'] = kb_resp['name']
                dataset['data'] = kb_resp['value']
                dataset['fill'] = False
                dataset['borderColor'] = colors[i%len(colors)]
                dataset['tension'] = 0.1
            elif plot_type == 'bar':
                dataset['label'] = kb_resp['name']
                dataset['data'] = kb_resp['value']
                dataset['backgroundColor'] = colors[i%len(colors)]
                dataset['borderWidth'] = 1
            datasets.append(dataset)
        # scatter? pie? maybe hist...

    response = {
        'labels': labels,
        'datasets': datasets
    }

    return response
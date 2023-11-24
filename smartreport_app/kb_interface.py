
def kb_interface(params):
    # kpi_list = params['kpi_list'] # id of the kpi in the kb
    plot_type = params['chart_type']
    # start_time = params['start_time']
    # end_time = params['end_time']
    # frequency = params['frequency']

    kpi_name = "pippo"

    if plot_type == 'line':
        response = {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            'datasets': [{
                'label': f'{kpi_name}',
                'data': [65, 59, 50, 40, 30, 20, 10],
                'fill': False,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.1
                }]
        }

    elif plot_type == 'bar':
        response = {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            'datasets': [{
                'label': f'{kpi_name}',
                'data': [20, 33, 45, 1, 34, 55, 40],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(201, 203, 207, 0.2)'
                ],
                'borderColor': [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)',
                    'rgb(201, 203, 207)',
                ],
                'borderWidth': 1
            }]
        }

    elif plot_type == 'scatter':
        response = {
            'datasets': [{
                'label': f'{kpi_name}',
                'data': [{'x': -10,'y': 0 }, 
                         {'x': 0,  'y': 10}, 
                         {'x': 10, 'y': 5 }, 
                         {'x': 0.5, 'y': 5.5 },
                         {'x': -10, 'y': -5},
                         {'x': -5, 'y': -10},
                         ],
                'backgroundColor': 'rgb(255, 99, 132)'
            }],
        }
    
    elif plot_type == 'pie' or plot_type == 'doughnut':
        response = {
            'labels': ['Good', 'Bad'],
            'datasets': [{
                'label': f'{kpi_name}',
                'data': [330, 60],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                ],
            'hoverOffset': 4
            }]
        }

    elif plot_type == 'radar':
        response = {
            'labels': [
                'Eating',
                'Drinking',
                'Sleeping',
                'Designing',
                'Coding',
                'Cycling',
                'Running'
            ],
            'datasets': [{
                'label': 'Yesterday',
                'data': [65, 59, 90, 81, 56, 55, 40],
                'fill': True,
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgb(255, 99, 132)',
                'pointBackgroundColor': 'rgb(255, 99, 132)',
                'pointBorderColor': '#fff',
                'pointHoverBackgroundColor': '#fff',
                'pointHoverBorderColor': 'rgb(255, 99, 132)'
            }, {
                'label': 'Today',
                'data': [28, 48, 40, 19, 96, 27, 100],
                'fill': True,
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgb(54, 162, 235)',
                'pointBackgroundColor': 'rgb(54, 162, 235)',
                'pointBorderColor': '#fff',
                'pointHoverBackgroundColor': '#fff',
                'pointHoverBorderColor': 'rgb(54, 162, 235)'
            }]
        }

    elif plot_type == 'scatter':
        response = {
            'datasets': [{
                'label': f'{kpi_name}',
                'data': [{'x': -10,'y': 0}, {'x': 0,'y': 10 }, {'x': 10,'y': 5},{'x': 0.5, 'y': 5.5
                }],
                'backgroundColor': 'rgb(255, 99, 132)'
            }],
        }
        

    return response
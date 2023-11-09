
def kb_interface(kpi_name, params):
    plot_type = params['chart_type']

    # other parameters like the time period

    if plot_type == 'line':
        response = {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            'data' : {
            'datasets': [{
                'label': 'massa di filippo',
                'data': [65, 59, 50, 40, 30, 20, 10],
                'fill': False,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.1
                }]
            }
        }

        return response

    elif plot_type == 'bar':
        response = {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            'datasets': [{
                'label': 'lunghezza del pene di paul',
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
        return response

    elif plot_type == 'scatter':
        response = {
            'datasets': [{
                'label': 'produzione di cagasburra',
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

        return response
    
    elif plot_type == 'pie' or plot_type == 'doughnut':
        response = {
            'labels': ['pene', 'muscoli'],
            'datasets': [{
                'label': 'composizione del corpo di paul',
                'data': [330, 60],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                ],
            'hoverOffset': 4
            }]
        }

        return response

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
                'label': 'ragnatela della mamma di filippo',
                'data': [65, 59, 90, 81, 56, 55, 40],
                'fill': True,
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgb(255, 99, 132)',
                'pointBackgroundColor': 'rgb(255, 99, 132)',
                'pointBorderColor': '#fff',
                'pointHoverBackgroundColor': '#fff',
                'pointHoverBorderColor': 'rgb(255, 99, 132)'
            }, {
                'label': 'ragnatela della mamma di paul',
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

        return response
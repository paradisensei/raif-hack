import random
import json

def random_hex_color() -> str:
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def gender_graph(gender) -> str:
    count = gender.size
    background_color = [random_hex_color() for _ in range(count)]

    graph_data = {
        'type': 'doughnut',
        'data': {
            'labels': list(gender.index.values),
            'datasets': [{
                'label': '',
                'data': list(gender.values.reshape(-1)),
                # 'backgroundColor': ['#4e73df', '#1cc88a', '#36b9cc'],
                'backgroundColor': background_color,
                'borderColor': ['#ffffff'] * count
            }],
        },
        'options': {
            'maintainAspectRatio': False,
            'legend': {'display': False, 'title': {}}
        }
    }

    return json.dumps(graph_data)

def avg_bill_graph(avg_bill) -> str:

    graph_data = {
        'type': 'line',
        'data': {
            'labels': list(map(lambda i: i[1].strftime('%Y-%m-%d'), list(avg_bill.index.values))),
            'datasets': [{
                'label': 'Earnings',
                'fill': True,
                'data': list(avg_bill.values.reshape(-1)),
                'backgroundColor': 'rgba(78, 115, 223, 0.05)',
                'borderColor': 'rgba(78, 115, 223, 1)'
            }],
        },
        'options': {
            'maintainAspectRatio': False,
            'legend': {'display': False},
            'title': {},
            'scales': {
                'xAxes': [{
                    'gridLines': {
                        'color': 'rgb(234, 236, 244)',
                        'zeroLineColor': 'rgb(234, 236, 244)',
                        'drawBorder': False,
                        'drawTicks': False,
                        'borderDash': [2],
                        'zeroLineBorderDash': [2],
                        'drawOnChartArea': False
                    },
                    'ticks': {
                        'fontColor': '#858796',
                        'padding': 20
                    }
                }],
                'yAxes': [{
                    'gridLines': {
                        'color': 'rgb(234, 236, 244)',
                        'zeroLineColor': 'rgb(234, 236, 244)',
                        'drawBorder': False,
                        'drawTicks': False,
                        'borderDash': [2],
                        'zeroLineBorderDash': [2]
                    },
                    'ticks': {
                        'fontColor': '#858796',
                        'padding': 20
                    }
                }]
            }
        }
    }

    return json.dumps(graph_data)
import random
import json

def random_hex_color() -> str:
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def avg_ltv(ltv):
    ltv_arr = list(ltv.values.reshape(-1))
    avg_ltv = sum(ltv_arr) / len(ltv_arr)
    return round(avg_ltv)

def gender_graph(gender) -> str:
    count = gender.size
    background_color = ['#4e73df', '#1cc88a', '#36b9cc']

    graph_data = {
        'type': 'doughnut',
        'data': {
            'labels': list(gender.index.values),
            'datasets': [{
                'label': '',
                'data': list(gender.values.reshape(-1)),
                'backgroundColor': background_color[:count],
                'borderColor': ['#ffffff'] * count
            }],
        },
        'options': {
            'maintainAspectRatio': False,
            'legend': {
                'position':'bottom', 
                'labels': {
                    'pointStyle': 'circle',
                    'usePointStyle': True
                }
            }
        }
    }

    return json.dumps(graph_data)

def age_graph(age) -> str:
    age.sort_index(inplace=True)
    count = age.size
    background_color = ['#f6c23e', '#e74a3b', '#4e73df', '#1cc88a', '#36b9cc']

    graph_data = {
        'type': 'doughnut',
        'data': {
            'labels': list(age.index.values),
            'datasets': [{
                'label': '',
                'data': list(age.values.reshape(-1)),
                'backgroundColor': background_color[:count],
                'borderColor': ['#ffffff'] * count
            }],
        },
        'options': {
            'maintainAspectRatio': False,
            'legend': {
                'position':'bottom', 
                'labels': {
                    'pointStyle': 'circle',
                    'usePointStyle': True
                }
            }
        }
    }

    return json.dumps(graph_data)

def avg_bill_graph(avg_bill) -> str:
    graph_data = {
        'type': 'line',
        'data': {
            'labels': list(map(lambda i: i.astype(str)[:10], list(avg_bill.index.values))),
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

def avg_tx_graph(avg_tx) -> str:
    graph_data = {
        'type': 'line',
        'data': {
            'labels': list(map(lambda i: i.astype(str)[:10], list(avg_tx.index.values))),
            'datasets': [{
                'label': 'Txs',
                'fill': True,
                'data': list(avg_tx.values.reshape(-1)),
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


def revenue_graph(revenue) -> str:
    graph_data = {
        'type': 'line',
        'data': {
            'labels': list(map(lambda i: i.astype(str)[:10], list(revenue.index.values))),
            'datasets': [{
                'label': 'Revenue',
                'fill': True,
                'data': list(revenue.values.reshape(-1)),
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


def income_in_segment(income_in_segment):
    max_income_in_segment = max(list(map(lambda iis: iis[2], income_in_segment)))

    bar_colors = ['bg-warning', 'bg-primary', 'bg-info', 'bg-success', 'bg-default']
    income_in_segment = list(map(lambda iis: (iis[0], round((iis[2]/max_income_in_segment)*100), round(iis[2]), bar_colors[iis[1]-1]), income_in_segment))
    return income_in_segment

def clients_in_segment(clients_in_segment):
    max_clients_in_segment = max(list(map(lambda cis: cis[2], clients_in_segment)))

    bar_colors = ['bg-warning', 'bg-primary', 'bg-info', 'bg-success', 'bg-default']
    clients_in_segment = list(map(lambda cis: (cis[0], round((cis[2]/max_clients_in_segment)*100), round(cis[2]), bar_colors[cis[1]-1]), clients_in_segment))
    return clients_in_segment

def tx_in_segment(tx_in_segment):
    max_tx_in_segment = max(list(map(lambda cis: cis[2], tx_in_segment)))

    bar_colors = ['bg-warning', 'bg-primary', 'bg-info', 'bg-success', 'bg-default']
    return list(map(lambda cis: (cis[0], round((cis[2]/max_tx_in_segment)*100), round(cis[2]), bar_colors[cis[1]-1]), tx_in_segment))


def top_client_segments(top_client_segments):
    segments = top_client_segments['segment'].tolist()
    revenue = top_client_segments['revenue'].tolist()
    return [(segments[i], round(revenue[i])) for i in range(len(segments))]

def top_churn_segments(top_churn_segments):
    print(top_churn_segments)
    segments = top_churn_segments['segment'].tolist()
    churn = top_churn_segments['class_1_proba'].tolist()
    return [(segments[i], round(float(churn[i])*100)) for i in range(len(segments))]

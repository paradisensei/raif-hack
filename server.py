from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request

import util
from backend import data_handling, metric_buttons

PATH_TO_LOADER_CSV_CONFIG = 'in/data_loader_csv_config.txt'
PATH_TO_LOADER_XLS_CONFIG = 'in/data_loader_xls_config.txt'

PATH_TO_MCC_COLUMNS = 'in/mcc_file_columns.txt'
PATH_TO_STORES_COLUMNS = 'in/stores_file_columns.txt'
PATH_TO_TRANSACTIONS_COLUMNS = 'in/transactions_file_columns.txt'
PATH_TO_CLIENTS_COLUMNS = 'in/clients_file_columns.txt'
PATH_TO_CLIENT_CATEGORIES_COLUMNS = 'in/client_categories_file_columns.txt'
PATH_TO_CLIENT_INTERNET_DATA_COLUMNS = 'in/client_internet_data_file_columns.txt'

PATH_TO_MCC_FILE = 'data/mcc.xlsx'
PATH_TO_STORES_FILE = 'data/stores.csv'
PATH_TO_TRANSACTIONS_FILE = 'data/transactions.csv'
PATH_TO_CLIENTS_FILE = 'data/clients.csv'
PATH_TO_CLIENT_CATEGORIES_FILE = 'data/client_categories.csv'
PATH_TO_CLIENT_INTERNET_DATA_FILE = 'data/client_internet_data.csv'

PATH_TO_CHURN_MODEL = 'in/churn_prediction_model.pickle'
PATH_TO_CHURN_MODEL_FEATURES = 'in/churn_prediction_model_features.pickle'
PATH_TO_FP_MODEL = 'in/fp_segmentation_model.pickle'
PATH_TO_FP_MODEL_FEATURES = 'in/fp_segmentation_model_features.pickle'

app = Flask(__name__, static_folder='assets')

@app.route('/')
def get_login() -> 'html':
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    # get store name and pass it to dashboard
    return redirect(url_for('dashboard', store=request.form['store']))

@app.route('/dashboard')
def dashboard() -> 'html':
    # get store from query string param
    store = request.args['store']

    # get start & end dates from query string params
    start_date = request.args.get('start_date')
    if start_date != None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%S.%f')
    end_date = request.args.get('end_date')
    if end_date != None:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%S.%f')

    # single-valued metrics
    avg_bill = round(metric_buttons.button_AverageBill(Transactions, Stores, store, start_date=start_date, end_date=end_date))
    ltv = metric_buttons.button_LTV(Transactions, Stores, store, start_date=start_date, end_date=end_date)
    client_count = metric_buttons.button_UniqueClientNumber(Transactions, Stores, store, start_date=start_date, end_date=end_date)

    # doughnut-graph metrics
    gender = metric_buttons.button_Gender(Transactions, Clients, Stores, store)
    age = metric_buttons.button_Age(Transactions, Clients, Stores, store)

    # # value-graph metrics
    client_avg_bill = metric_buttons.button_ClientAverageBill(Transactions, Stores, store, start_date=start_date, end_date=end_date)
    client_avg_tx = metric_buttons.button_AverageTransactionNumber(Transactions, Stores, store, start_date=start_date, end_date=end_date)
    client_revenue = metric_buttons.button_RevenueDynamicByDay(Transactions, Stores, store, start_date=start_date, end_date=end_date)

    return render_template(
        'index.html',
        store=store,
        avg_ltv=util.avg_ltv(ltv),
        avg_bill=avg_bill,
        client_count=client_count,
        gender=util.gender_graph(gender),
        age=util.age_graph(age),
        client_avg_bill=util.avg_bill_graph(client_avg_bill),
        client_avg_tx=util.avg_tx_graph(client_avg_tx),
        client_revenue=util.revenue_graph(client_revenue),
        income_in_segment=income_in_segment,
        clients_in_segment=clients_in_segment,
        tx_in_segment=tx_in_segment
    )


if __name__ == "__main__":
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    Transactions = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))

    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_STORES_COLUMNS)
    Stores = data_handling.data_loader(columns, PATH_TO_STORES_FILE, dict(params))

    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_CLIENTS_COLUMNS)
    Clients = data_handling.data_loader(columns, PATH_TO_CLIENTS_FILE, dict(params))
    
    #churn_model = data_handling.load_from_pickle(PATH_TO_CHURN_MODEL)
    #churn_model_features = data_handling.load_from_pickle(PATH_TO_CHURN_MODEL_FEATURES)
    
    fp_model = data_handling.load_from_pickle(PATH_TO_FP_MODEL)
    fp_model_features = data_handling.load_from_pickle(PATH_TO_FP_MODEL_FEATURES)

    # pre-calculate rating-graph metrics
    s = 'Fix Price'
    income_in_segment = util.income_in_segment(metric_buttons.button_IncomeInSegmentRate(Transactions, Stores, s)[1:])
    clients_in_segment = util.clients_in_segment(metric_buttons.button_ClientNumberInSegmentRate(Transactions, Stores, s)[1:])
    tx_in_segment = util.tx_in_segment(metric_buttons.button_TransactionNumberInSegmentRate(Transactions, Stores, s)[1:])

    app.run(debug=True)

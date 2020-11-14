from flask import Flask, render_template, redirect, url_for, request
import json
import util
from backend import data_handling, metric_buttons
import numpy as np
import pandas as pd
import sys, os, random, re, datetime
from imp import reload

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



app = Flask(__name__, static_folder='assets')

@app.route('/')
def get_login() -> 'html':
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    # get merchant name and pass it to dashboard
    return redirect(url_for('dashboard', merchant=request.form['merchant']))

@app.route('/dashboard')
def dashboard() -> 'html':
    # get merchant from param
    merchant = request.args['merchant']

    # single-valued metrics
    avg_bill = round(metric_buttons.button_AverageBill(Transactions, Stores))
    ltv = metric_buttons.button_LTV(Transactions, Stores)

    # doughnut-graph metrics
    gender = metric_buttons.button_Gender(Transactions, Clients, Stores)
    age = metric_buttons.button_Age(Transactions, Clients, Stores)

    # # value-graph metrics
    client_avg_bill = metric_buttons.button_ClientAverageBill(Transactions, Stores)
    client_avg_tx = metric_buttons.button_AverageTransactionNumber(Transactions, Stores)

    # # rating-graph metrics
    income_in_segment = metric_buttons.button_IncomeInSegmentRate(Transactions, Stores, merchant)[1:]
    clients_in_segment = metric_buttons.button_ClientNumberInSegmentRate(Transactions, Stores, merchant)[1:]

    return render_template(
        'index.html',
        merchant=merchant,
        avg_ltv = util.avg_ltv(ltv),
        avg_bill=avg_bill,
        gender=util.gender_graph(gender),
        age=util.age_graph(age),
        client_avg_bill=util.avg_bill_graph(client_avg_bill),
        client_avg_tx=util.avg_tx_graph(client_avg_tx),
        income_in_segment=util.income_in_segment(income_in_segment),
        clients_in_segment=util.clients_in_segment(clients_in_segment),
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
    
    app.run(debug=True)
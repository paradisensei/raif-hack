import numpy as np
import pandas as pd
import sys, os, random, re, datetime
from imp import reload

sys.path.append('.')
from . import data_handling; reload(data_handling);
from . import metrics; reload(metrics);

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



def button_NewClientTransactions(start_date=None, end_date=None):
    '''
    in:
    start_date: datetime
    start_date: datetime
    
    out:
    int
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.NewClientTransactions(df, start_date, end_date)

def button_ClientAverageBill(merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    pd.Series(index=CNUM, data=mean(Amount))
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.ClientAverageBill(df, merchant_name, start_date, end_date, clients)

def button_AverageBill(start_date=None, end_date=None):
    '''
    in:
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.AverageBill(df, start_date, end_date)

def button_AverageTransactionNumber(merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.AverageTransactionNumber(df, merchant_name, start_date, end_date, clients)

def button_Revenue(merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.Revenue(df, merchant_name, start_date, end_date, clients)
    
def button_RevenueDynamicByDay(merchants=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchants: list of str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.RevenueDynamicByDay(df, merchants, start_date, end_date, clients)

def button_IncomeInSegmentRate(merchant_name, competitor_merchants=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    competitor_merchants: list-like of str
    n: int
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.IncomeInSegmentRate(df, merchant_name, competitor_merchants, n, start_date, end_date, clients)

def button_ClientNumberInSegmentRate(merchant_name, competitor_merchants=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    competitor_merchants: list-like of str
    n: int
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.ClientNumberInSegmentRate(df, merchant_name, competitor_merchants, n, start_date, end_date, clients)
    
def button_TransactionNumberInSegmentRate(merchant_name, competitor_merchants=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    competitor_merchants: list-like of str
    n: int
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.TransactionNumberInSegmentRate(df, merchant_name, competitor_merchants, n, start_date, end_date, clients)

def button_Gender():
    '''
    in:
    None
    
    out:
    pd.Series(index=Gender, data=value_counts(normalize=True))
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df1 = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_CLIENTS_COLUMNS)
    df2 = data_handling.data_loader(columns, PATH_TO_CLIENTS_FILE, dict(params))
    
    return metrics.Gender(df1, df2)

def button_Age():
    '''
    in:
    None
    
    out:
    pd.Series(index=Age_group, data=value_counts(normalize=True))
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df1 = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_CLIENTS_COLUMNS)
    df2 = data_handling.data_loader(columns, PATH_TO_CLIENTS_FILE, dict(params))
    
    return metrics.Age(df1, df2)
    
def button_AmountByGender(f=np.sum):
    '''
    in:
    f: object
    
    out:
    pd.Series(index=Gender, data=f(Amount))
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df1 = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_CLIENTS_COLUMNS)
    df2 = data_handling.data_loader(columns, PATH_TO_CLIENTS_FILE, dict(params))
    
    return metrics.AmountByGender(df1, df2, f)

def button_AverageBillByAge(f=np.mean):
    '''
    in:
    f: object
    
    out:
    pd.Series(index=Age, data=f(Amount))
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df1 = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_CLIENTS_COLUMNS)
    df2 = data_handling.data_loader(columns, PATH_TO_CLIENTS_FILE, dict(params))
    
    return metrics.AverageBillByAge(df1, df2, f)

def button_LTV(merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    clients: list-like
    
    out:
    pd.Series(index=CNUM, data=LTV)
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.LTV(df, merchant_name, start_date, end_date, clients)

def button_Retention(merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    clients: list-like
    
    out:
    pd.DataFrame
    '''
    
    params = data_handling.read_loader_config(PATH_TO_LOADER_CSV_CONFIG)
    columns = data_handling.read_file_columns(PATH_TO_TRANSACTIONS_COLUMNS)
    df = data_handling.data_loader(columns, PATH_TO_TRANSACTIONS_FILE, dict(params))
    
    return metrics.Retention(df, merchant_name, start_date, end_date, clients)

def button_MostPayableSegments():
    '''
    in:
    
    out:
    
    '''
    
    return None
    
    

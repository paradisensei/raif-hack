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



def button_UniqueClientNumber(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime
    start_date: datetime
    
    out:
    int
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.UniqueClientNumber(Transactions)

def button_NewClientTransactions(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime
    start_date: datetime
    
    out:
    int
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.NewClientTransactions(Transactions)

def button_ClientAverageBill(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    pd.Series(index=CNUM, data=mean(Amount))
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond4 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3&cond4]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.ClientAverageBill(Transactions)

def button_AverageBill(Transactions, Stores, store_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1&cond2&cond3]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.AverageBill(Transactions)

def button_AverageTransactionNumber(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond4 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3&cond4]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.AverageTransactionNumber(Transactions)

def button_Revenue(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond4 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond5 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond4&cond5]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] < start_date
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    
    return metrics.Revenue(Transactions[cond1], Transactions[cond2&cond3])
    
def button_RevenueDynamicByDay(Transactions, Stores, store_name=None, merchants=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchants: list of str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond4 = pd.Series(True, index=Transactions.index) if merchants is None else Transactions['MerchantName'].isin(merchants)
    Transactions = Transactions[cond1&cond2&cond3&cond4]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.RevenueDynamicByDay(Transactions)

def button_IncomeInSegmentRate(Transactions, Stores, store_name, competitor_stores=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    competitor_stores: list-like of str
    n: int
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    Transactions = Transactions[cond1&cond2&cond3]
    
    cond1 = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions_store = pd.merge(Transactions, Stores[cond1], how='inner', on='MerchantName')
    
    cond1 = pd.Series(True, index=Stores.index) if competitor_stores is None else Stores['StoreName'].isin(competitor_stores)
    Transactions_competitors = pd.merge(Transactions, Stores[cond1], how='inner', on='MerchantName')
    
    return metrics.IncomeInSegmentRate(Transactions_store, Transactions_competitors, n)

def button_ClientNumberInSegmentRate(Transactions, Stores, store_name, competitor_stores=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    competitor_stores: list-like of str
    n: int
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    Transactions = Transactions[cond1&cond2&cond3]
    
    cond1 = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions_store = pd.merge(Transactions, Stores[cond1], how='inner', on='MerchantName')
    
    cond1 = pd.Series(True, index=Stores.index) if competitor_stores is None else Stores['StoreName'].isin(competitor_stores)
    Transactions_competitors = pd.merge(Transactions, Stores[cond1], how='inner', on='MerchantName')
    
    return metrics.ClientNumberInSegmentRate(Transactions_store, Transactions_competitors, n)
    
def button_TransactionNumberInSegmentRate(Transactions, Stores, store_name, competitor_stores=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    competitor_stores: list-like of str
    n: int
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    Transactions = Transactions[cond1&cond2&cond3]
    
    cond1 = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions_store = pd.merge(Transactions, Stores[cond1], how='inner', on='MerchantName')
    
    cond1 = pd.Series(True, index=Stores.index) if competitor_stores is None else Stores['StoreName'].isin(competitor_stores)
    Transactions_competitors = pd.merge(Transactions, Stores[cond1], how='inner', on='MerchantName')
    
    return metrics.TransactionNumberInSegmentRate(Transactions_store, Transactions_competitors, n)

def button_Gender(Transactions, Clients, Stores, store_name=None):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    
    out:
    pd.Series(index=Gender, data=value_counts(normalize=True))
    '''
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    Transactions = pd.merge(Transactions, Clients[['CNUM','Gender']], how='inner', on='CNUM')
    
    return metrics.Gender(Transactions)

def button_Age(Transactions, Clients, Stores, store_name=None):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    
    out:
    pd.Series(index=Gender, data=value_counts(normalize=True))
    '''
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    Transactions = pd.merge(Transactions, Clients[['CNUM','Age']], how='inner', on='CNUM')
    
    return metrics.Age(Transactions)
    
def button_AmountByGender(Transactions, Clients, Stores, store_name=None, f=np.sum):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    f: object
    
    out:
    pd.Series(index=Gender, data=f(Amount))
    '''
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    Transactions = pd.merge(Transactions, Clients[['CNUM','Gender']], how='inner', on='CNUM')
    
    return metrics.AmountByGender(Transactions, f)

def button_AverageBillByAge(Transactions, Clients, Stores, store_name=None, f=np.mean):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    f: object
    
    out:
    pd.Series(index=Age, data=f(Amount))
    '''
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    Transactions = pd.merge(Transactions, Clients[['CNUM','Age']], how='inner', on='CNUM')
    
    return metrics.AverageBillByAge(Transactions, f)

def button_LTV(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    clients: list-like
    
    out:
    pd.Series(index=CNUM, data=LTV)
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond4 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3&cond4]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.LTV(Transactions)

def button_Retention(Transactions, Stores, store_name=None, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    Stores: pd.DataFrame
    store_name: str
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    clients: list-like
    
    out:
    pd.Series(index=CNUM, data=LTV)
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond4 = pd.Series(True, index=Transactions.index) if merchants is None else Transactions['MerchantName'].isin(merchants)
    Transactions = Transactions[cond1&cond2&cond3&cond4]
    
    cond = pd.Series(True, index=Stores.index) if store_name is None else Stores['StoreName'] == store_name
    Transactions = pd.merge(Transactions, Stores[cond], how='inner', on='MerchantName')
    
    return metrics.Retention(Transactions)

def button_MostPayableSegments():
    '''
    in:
    
    out:
    
    '''
    
    return None
    
    

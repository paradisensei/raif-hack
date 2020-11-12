import numpy as np
import pandas as pd
import sys, os, random, re, datetime



def NewClientTransactions(Transactions, start_date=None, end_date=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime
    start_date: datetime
    
    out:
    int
    '''
    
    freq = Transactions.groupby('CNUM')['Amount'].count().reset_index()
    freq = freq.rename({'Amount':'Frequency'}, axis=1)
    freq = freq[freq['Frequency']==1]
    
    cond1 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond2 = 1 if end_date is None else Transactions['Date'] <= end_date
    Transactions = pd.merge(Transactions[cond1&cond2], freq, how='inner', on='CNUM')
    
    return Transactions.shape[0]

def ClientAverageBill(Transactions, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    pd.Series(index=CNUM, data=mean(Amount))
    '''
    
    cond1 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond2 = 1 if end_date is None else Transactions['Date'] <= end_date
    cond3 = 1 if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1&cond2&cond3].groupby('CNUM')['Amount'].mean()
    
    return Transactions

def AverageBill(Transactions, start_date=None, end_date=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond2 = 1 if end_date is None else Transactions['Date'] <= end_date
    Transactions = Transactions[cond1&cond2]
    n = Transactions['CNUM'].nunique() * 1.0
    
    return Transactions['Amount'].sum() / n if n != 0 else np.nan

def AverageTransactionNumber(Transactions, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond2 = 1 if end_date is None else Transactions['Date'] <= end_date
    cond3 = 1 if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1&cond2&cond3]
    
    return Transactions.groupby('CNUM')['Amount'].count().mean()

def Revenue(Transactions, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond4 = 1 if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond4]
    cond1 = 1 if start_date is None else Transactions['Date'] < start_date
    cond2 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond3 = 1 if end_date is None else Transactions['Date'] <= end_date
    
    a = Transactions[cond2&cond3]['Amount'].sum()
    b = Transactions[cond1]['Amount'].sum()
    
    return ((a-b) / b)*100.0 if b != 0 else np.nan

def IncomeInSegmentRate(Transactions, merchant_name, competitor_merchants, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    competitor_merchants: list-like of str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond4 = 1 if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond4]
    cond1 = 1 if start_date is None else Transactions['Date'] < start_date
    cond2 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond3 = 1 if end_date is None else Transactions['Date'] <= end_date
    cond5 = Transactions['MerchantName'] == merchant_name
    cond6 = Transactions['MerchantName'].isin(competitor_merchants)
    
    a = Transactions[cond2&cond3&cond5]['Amount'].sum()
    b = Transactions[cond1&cond5]['Amount'].sum()
    s1 = ((a-b) / b)*100.0 if b != 0 else np.nan
    
    c = Transactions[cond2&cond3&cond6]['Amount'].sum()
    d = Transactions[cond1&cond6]['Amount'].sum()
    s2 = ((c-d) / d)*100.0 if d != 0 else np.nan
    
    return s1/s2 if s2 != 0 else np.nan

def ClientNumberInSegmentRate(Transactions, merchant_name, competitor_merchants, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    competitor_merchants: list-like of str
    start_date: datetime
    start_date: datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = 1 if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1]
    cond2 = 1 if start_date is None else Transactions['Date'] >= start_date
    cond3 = 1 if end_date is None else Transactions['Date'] <= end_date
    cond4 = Transactions['MerchantName'] == merchant_name
    cond5 = Transactions['MerchantName'].isin(competitor_merchants)
    
    a = Transactions[cond2&cond3&cond4]['CNUM'].count()
    b = Transactions[cond2&cond3&cond5]['CNUM'].count()
    
    return a/b if b != 0 else np.nan

def Gender(Transactions, Clients, f=np.sum):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    
    out:
    pd.Series(index=Gender, data=f(Amount))
    '''
    
    Transactions = pd.merge(Transactions, Clients[['CNUM','Gender']], how='inner', on='CNUM')
    
    return Transactions.groupby('Gender')['Amount'].agg([f])

def Age(Transactions, Clients, f=np.mean):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    
    out:
    pd.Series(index=Gender, data=f(Amount))
    '''
    
    Transactions = pd.merge(Transactions, Clients[['CNUM','Age']], how='inner', on='CNUM')
    
    return Transactions.groupby('Age')['Amount'].agg([f])

def LTV():
    '''
    in:
    
    out:
    
    '''
    
    return None

def Retention():
    '''
    in:
    
    out:
    
    '''
    
    return None

def MostPayableSegments():
    '''
    in:
    
    out:
    
    '''
    
    return None
import numpy as np
import pandas as pd
import sys, os, random, re, datetime
from operator import attrgetter
from imp import reload

sys.path.append('.')
from . import tree_utils; reload(tree_utils);



def NewClientTransactions(Transactions, start_date=None, end_date=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime.datetime
    end_date: datetime.datetime
    
    out:
    int
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    Transactions = Transactions[cond1&cond2]
    
    Transactions = Transactions.groupby('CNUM')['Amount'].count().reset_index()
    Transactions = Transactions[Transactions['Amount']==1]
    
    return Transactions.shape[0]

def ClientAverageBill(Transactions, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    pd.Series(index=CNUM, data=mean(Amount))
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond4 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3&cond4].groupby(['CNUM','Date'])['Amount'].mean()
    
    return Transactions

def AverageBill(Transactions, start_date=None, end_date=None):
    '''
    in:
    Transactions: pd.DataFrame
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    float
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    Transactions = Transactions[cond1&cond2]
    n = Transactions['CNUM'].nunique() * 1.0
    
    return Transactions['Amount'].sum() / n if n != 0 else np.nan

def AverageTransactionNumber(Transactions, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    pd.Series(index=Date, data=count(CNUM)/nunique(CNUM))
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond2 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond3 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond4 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    
    gr1 = Transactions[cond1&cond2&cond3&cond4].groupby('Date')['CNUM'].nunique()
    gr2 = Transactions[cond1&cond2&cond3&cond4].groupby('Date')['CNUM'].count()
    
    return gr2 / gr1

def Revenue(Transactions, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    pd.Series(index=Date, data=float)
    '''
    
    cond4 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond4]
    cond1 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] < start_date
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond5 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    
    a = Transactions[cond2&cond3&cond5].groupby('Date')['Amount'].sum()
    b = Transactions[cond1&cond5].groupby('Date')['Amount'].sum()
    
    return ((a-b) / b)*100.0
    
def RevenueDynamicByDay(Transactions, merchants=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchants: list of str
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    pd.Series(index=Date, data=float)
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1]
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond4 = pd.Series(True, index=Transactions.index) if merchants is None else Transactions['MerchantName'].isin(merchants)
    
    a = Transactions[cond2&cond3&cond4].groupby('Date')['Amount'].sum()
    
    return a

def IncomeInSegmentRate(Transactions, merchant_name, competitor_merchants=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    competitor_merchants: list-like of str
    n: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    list of tuples(int, MerchantName, sum(Amount))
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1]
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] < start_date
    cond3 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond4 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond5 = Transactions['MerchantName'] == merchant_name
    cond6 = pd.Series(True, index=Transactions.index) if competitor_merchants is None else Transactions['MerchantName'].isin(competitor_merchants)
    
    c = 'Amount'
    s1 = Transactions[cond3&cond4&cond5].groupby('MerchantName')[c].sum().reset_index()
    s2 = Transactions[cond3&cond4&cond6].groupby('MerchantName')[c].sum().reset_index()
    s1 = pd.concat([s1,s2], axis=0, ignore_index=True, sort=False).drop_duplicates().sort_values(c, ascending=False).reset_index(drop=True)
    
    rating = [(merchant_name, int(s1[s1['MerchantName']==merchant_name].index.values)+1, int(s1[s1['MerchantName']==merchant_name][c].values))]
    s1 = s1.head(n)
    rating += [(i,j+1,k) for i,j,k in zip(s1['MerchantName'].values, s1.index, s1[c].values)]
    
    return rating

def ClientNumberInSegmentRate(Transactions, merchant_name, competitor_merchants=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    competitor_merchants: list-like of str
    n: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    list of tuples(int, MerchantName, nunique(CNUM))
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1]
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] < start_date
    cond3 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond4 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond5 = Transactions['MerchantName'] == merchant_name
    cond6 = pd.Series(True, index=Transactions.index) if competitor_merchants is None else Transactions['MerchantName'].isin(competitor_merchants)
    
    c = 'CNUM'
    s1 = Transactions[cond3&cond4&cond5].groupby('MerchantName')[c].nunique().reset_index()
    s2 = Transactions[cond3&cond4&cond6].groupby('MerchantName')[c].nunique().reset_index()
    s1 = pd.concat([s1,s2], axis=0, ignore_index=True, sort=False).drop_duplicates().sort_values(c, ascending=False).reset_index(drop=True)
    
    rating = [(merchant_name, int(s1[s1['MerchantName']==merchant_name].index.values)+1, int(s1[s1['MerchantName']==merchant_name][c].values))]
    s1 = s1.head(n)
    rating += [(i,j+1,k) for i,j,k in zip(s1['MerchantName'].values, s1.index, s1[c].values)]
    
    return rating
    
def TransactionNumberInSegmentRate(Transactions, merchant_name, competitor_merchants=None, n=5, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    competitor_merchants: list-like of str
    n: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    cliets: list-like
    
    out:
    list of tuples(int, MerchantName, count(CNUM))
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    Transactions = Transactions[cond1]
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] < start_date
    cond3 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond4 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond5 = Transactions['MerchantName'] == merchant_name
    cond6 = pd.Series(True, index=Transactions.index) if competitor_merchants is None else Transactions['MerchantName'].isin(competitor_merchants)
    
    c = 'CNUM'
    s1 = Transactions[cond3&cond4&cond5].groupby('MerchantName')[c].count().reset_index()
    s2 = Transactions[cond3&cond4&cond6].groupby('MerchantName')[c].count().reset_index()
    s1 = pd.concat([s1,s2], axis=0, ignore_index=True, sort=False).drop_duplicates().sort_values(c, ascending=False).reset_index(drop=True)
    
    rating = [(merchant_name, int(s1[s1['MerchantName']==merchant_name].index.values)+1, int(s1[s1['MerchantName']==merchant_name][c].values))]
    s1 = s1.head(n)
    rating += [(i,j+1,k) for i,j,k in zip(s1['MerchantName'].values, s1.index, s1[c].values)]
    
    return rating

def Gender(Transactions, Clients, f=np.sum):
    '''
    in:
    Transactions: pd.DataFrame
    Clients: pd.DataFrame
    f: object
    
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
    f: object
    
    out:
    pd.Series(index=Gender, data=f(Amount))
    '''
    
    Transactions = pd.merge(Transactions, Clients[['CNUM','Age']], how='inner', on='CNUM')
    
    return Transactions.groupby('Age')['Amount'].agg([f])

def LTV(Transactions, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
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
    
    #lifespan = (Transactions.groupby("CNUM")['Date'].max() - Transactions.groupby("CNUM")['Date'].min()).apply(lambda x: x.days)
    #lifespan = lifespan * 1.0 / 365
    average_transactions_per_year = Transactions.groupby('CNUM')['Amount'].count() # / lifespan
    average_transaction_amount = Transactions.groupby('CNUM')['Amount'].mean()
    
    ltv = average_transactions_per_year * average_transaction_amount # * lifespan
    
    return ltv

def Retention(Transactions, merchant_name=None, start_date=None, end_date=None, clients=None):
    '''
    in:
    Transactions: pd.DataFrame
    merchant_name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    clients: list-like
    
    out:
    pd.DataFrame
    '''
    
    cond1 = pd.Series(True, index=Transactions.index) if clients is None else Transactions['CNUM'].isin(clients)
    cond2 = pd.Series(True, index=Transactions.index) if start_date is None else Transactions['Date'] >= start_date
    cond3 = pd.Series(True, index=Transactions.index) if end_date is None else Transactions['Date'] <= end_date
    cond4 = pd.Series(True, index=Transactions.index) if merchant_name is None else Transactions['MerchantName'] == merchant_name
    Transactions = Transactions[cond1&cond2&cond3&cond4]
    
    Transactions['transaction_month'] = Transactions['Date'].dt.to_period('M')
    Transactions['cohort'] = Transactions.groupby('CNUM')['Date'].transform('min').dt.to_period('M')
    
    Transactions = Transactions.groupby(['cohort','transaction_month']).agg({'CNUM':[('n_customers', 'nunique')]}).reset_index(drop=False)
    Transactions['n_customers'] = Transactions['CNUM'].values
    Transactions['period_number'] = (Transactions['transaction_month'] - Transactions['cohort']) #.apply(attrgetter('n'))
    
    cohort_pivot = Transactions.pivot_table(index='cohort', columns='period_number', values='n_customers')
    del Transactions

    cohort_size = cohort_pivot.iloc[:,0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    
    return retention_matrix

def MostProbableSegments():
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
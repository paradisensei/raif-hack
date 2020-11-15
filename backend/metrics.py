import numpy as np
import pandas as pd
import sys, os, random, re, datetime
from operator import attrgetter
from imp import reload

sys.path.append('.')
from . import tree_utils; reload(tree_utils);



def CompetitorsNumber(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    int
    '''
    
    return Transactions['StoreName'].unique().shape[0]-1

def UniqueClientNumber(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    int
    '''
    
    return Transactions['CNUM'].unique().shape[0]

def NewClientTransactions(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    int
    '''
    
    Transactions = Transactions.groupby('CNUM')['Amount'].count().reset_index()
    Transactions = Transactions[Transactions['Amount']==1]
    
    return Transactions.shape[0]

def ClientAverageBill(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.Series(index=CNUM, data=mean(Amount))
    '''
    
    return Transactions.groupby('Date')['Amount'].mean()

def AverageBill(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    float
    '''
    
    #n = Transactions['CNUM'].nunique() * 1.0
    #return Transactions['Amount'].sum() / n if n != 0 else np.nan
    return Transactions['Amount'].mean()

def AverageTransactionNumber(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.Series(index=Date, data=count(CNUM)/nunique(CNUM))
    '''
    
    gr1 = Transactions.groupby('Date')['CNUM'].nunique()
    gr2 = Transactions.groupby('Date')['CNUM'].count()
    
    return (gr2 / gr1).sort_index(ascending=True)

def Revenue(Transactions_prev, Transactions_next):
    '''
    in:
    Transactions_prev: pd.DataFrame
    Transactions_next: pd.DataFrame
    
    out:
    pd.Series(index=Date, data=float)
    '''
    
    a = Transactions_next.groupby('Date')['Amount'].sum()
    b = Transactions_prev.groupby('Date')['Amount'].sum()
    a = ((a-b) / b)*100.0
    
    return a.sort_index(ascending=True)
    
def RevenueDynamicByDay(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.Series(index=Date, data=float)
    '''
    
    return Transactions.groupby('Date')['Amount'].sum()

def IncomeInSegmentRate(Transactions_store, Transactions_competitors, n):
    '''
    in:
    Transactions_store: pd.DataFrame
    Transactions_competitors: pd.DataFrame
    n: int
    
    out:
    list of tuples(int, StoreName, sum(Amount))
    '''
    
    c = 'Amount'
    f = 'StoreName'
    store_name = Transactions_store[f].unique()[0]
    
    s1 = Transactions_store.groupby(f)[c].sum().reset_index()
    s2 = Transactions_competitors.groupby(f)[c].sum().reset_index()
    s1 = pd.concat([s1,s2], axis=0, ignore_index=True, sort=False).drop_duplicates().sort_values(c, ascending=False).reset_index(drop=True)
    
    rating = [(store_name, int(s1[s1[f]==store_name].index.values)+1, int(s1[s1[f]==store_name][c].values))]
    s1 = s1.head(n)
    rating += [(i,j+1,k) for i,j,k in zip(s1[f].values, s1.index, s1[c].values)]
    
    return rating

def ClientNumberInSegmentRate(Transactions_store, Transactions_competitors, n):
    '''
    in:
    Transactions_store: pd.DataFrame
    Transactions_competitors: pd.DataFrame
    n: int
    
    out:
    list of tuples(int, StoreName, nunique(CNUM))
    '''
    
    c = 'CNUM'
    f = 'StoreName'
    store_name = Transactions_store[f].unique()[0]
    
    s1 = Transactions_store.groupby(f)[c].nunique().reset_index()
    s2 = Transactions_competitors.groupby(f)[c].nunique().reset_index()
    s1 = pd.concat([s1,s2], axis=0, ignore_index=True, sort=False).drop_duplicates().sort_values(c, ascending=False).reset_index(drop=True)
    
    rating = [(store_name, int(s1[s1[f]==store_name].index.values)+1, int(s1[s1[f]==store_name][c].values))]
    s1 = s1.head(n)
    rating += [(i,j+1,k) for i,j,k in zip(s1[f].values, s1.index, s1[c].values)]
    
    return rating
    
def TransactionNumberInSegmentRate(Transactions_store, Transactions_competitors, n):
    '''
    in:
    Transactions_store: pd.DataFrame
    Transactions_competitors: pd.DataFrame
    n: int
    
    out:
    list of tuples(int, StoreName, count(CNUM))
    '''
    
    c = 'CNUM'
    f = 'StoreName'
    store_name = Transactions_store[f].unique()[0]
    
    s1 = Transactions_store.groupby(f)[c].count().reset_index()
    s2 = Transactions_competitors.groupby(f)[c].count().reset_index()
    s1 = pd.concat([s1,s2], axis=0, ignore_index=True, sort=False).drop_duplicates().sort_values(c, ascending=False).reset_index(drop=True)
    
    rating = [(store_name, int(s1[s1[f]==store_name].index.values)+1, int(s1[s1[f]==store_name][c].values))]
    s1 = s1.head(n)
    rating += [(i,j+1,k) for i,j,k in zip(s1[f].values, s1.index, s1[c].values)]
    
    return rating

def Gender(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.Series(index=Gender, data=value_counts(normalize=True))
    '''
    
    return Transactions['Gender'].value_counts(normalize=True)

def Age(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.Series(index=Age_group, data=value_counts(normalize=True))
    '''
    
    Transactions['Age_group'] = Transactions['Age'].apply(lambda x: '0-20' if x<=20 else
                                                                    '20-30' if x<=30 else
                                                                    '30-40' if x<=40 else
                                                                    '40-50' if x<=50 else
                                                                    '50-60' if x<=60 else
                                                                    '60+'
                                                         )
    
    return Transactions['Age_group'].value_counts(normalize=True)
    
def AmountByGender(Transactions, f=np.sum):
    '''
    in:
    Transactions: pd.DataFrame
    f: object
    
    out:
    pd.Series(index=Gender, data=f(Amount))
    '''
    
    return Transactions.groupby('Gender')['Amount'].agg([f])

def AverageBillByAge(Transactions, f=np.mean):
    '''
    in:
    Transactions: pd.DataFrame
    f: object
    
    out:
    pd.Series(index=Age, data=f(Amount))
    '''
    
    return Transactions.groupby('Age')['Amount'].agg([f])

def LTV(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.Series(index=CNUM, data=LTV)
    '''
    
    #lifespan = (Transactions.groupby("CNUM")['Date'].max() - Transactions.groupby("CNUM")['Date'].min()).apply(lambda x: x.days)
    #lifespan = lifespan * 1.0 / 365
    average_transactions_per_year = Transactions.groupby('CNUM')['Amount'].count() # / lifespan
    average_transaction_amount = Transactions.groupby('CNUM')['Amount'].mean()
    
    ltv = average_transactions_per_year * average_transaction_amount # * lifespan
    
    return ltv

def Retention(Transactions):
    '''
    in:
    Transactions: pd.DataFrame
    
    out:
    pd.DataFrame
    '''
    
    Transactions['transaction_month'] = Transactions['Date'].dt.to_period('M')
    Transactions['cohort'] = Transactions.groupby('CNUM')['Date'].transform('min').dt.to_period('M')
    
    Transactions = Transactions.groupby(['cohort','transaction_month']).agg({'CNUM':[('n_customers', 'nunique')]}).reset_index(drop=False)
    Transactions['n_customers'] = Transactions['CNUM'].values
    Transactions['period_number'] = (Transactions['transaction_month'] - Transactions['cohort']) #.apply(attrgetter('n'))
    
    cohort_pivot = Transactions.pivot_table(index='cohort', columns='period_number', values='n_customers')
    #del Transactions

    cohort_size = cohort_pivot.iloc[:,0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    
    return retention_matrix

def MostPayableSegments(model, feature_names, n=5):
    '''
    in:
    model: object
    feature_names: list-like
    n: int
    
    out:
    pd.DataFrame
    '''
    
    try:
        segments = tree_utils.get_most_probable_regression_ensemble_paths(model, feature_names, n)
    except:
        segments = tree_utils.get_most_probable_regression_tree_paths(model, feature_names, n)
    
    return segments
    
def ChurnSegments(model, feature_names, n=5):
    '''
    in:
    model: object
    feature_names: list-like
    n: int
    
    out:
    pd.DataFrame
    '''
    
    try:
        segments = tree_utils.get_most_probable_classification_ensemble_paths(model, feature_names, n)
    except:
        segments = tree_utils.get_most_probable_classification_tree_paths(model, feature_names, n)
    
    return segments
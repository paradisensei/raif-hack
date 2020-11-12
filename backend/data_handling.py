import numpy as np
import pandas as pd
import sys, os, random, re, datetime



def read_loader_config(path_to_file):
    '''
    in:
    path_to_file: str
    
    out:
    dict
    '''
    
    df = pd.read_csv(path_to_file, sep='\t', header=None)
    return {k:v for k,v in zip(df[0],df[1])}

def read_file_columns(path_to_file):
    '''
    in:
    path_to_file: str
    
    out:
    list
    '''
    
    with open(path_to_file, 'r') as f:
        columns = [line.strip() for line in f.readlines()]
    return columns
    
def data_loader(columns, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                db_connection_parameters=None):
        '''
        in:
        columns: list
        path_to_file: str
        reading_parameters: dict
        db_connection_parameters: dict
        
        out:
        pd.DataFrame
        '''
    
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            pass
        
        else:
            if reading_parameters['extension'] in ['.csv','csv']:
                _ = reading_parameters.pop('extension')
                df = pd.read_csv(path_to_file, **reading_parameters)

            elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
                _ = reading_parameters.pop('extension')
                df = pd.read_excel(path_to_file, **reading_parameters)
            
            if set(list(df.columns)).intersection(set(columns)) != set(columns):
                return "Error: can't find needed columns in data"
            
            return df[columns]

class data_loader_mcc(object):
    def __init__(self):
        self.columns = ['MCC','CategoryName']
    
    def load_data(self, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                        db_connection_parameters=None):
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            return self.load_data_from_db(db_connection_parameters)
        else:
            return self.load_data_from_local(path_to_file, reading_parameters)
    
    def load_data_from_local(self, path_to_file, reading_parameters):
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns)) != set(self.columns):
            return "Error: can't find needed columns in data"
            
        return df[self.columns]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_stores(object):
    def __init__(self):
        self.columns = ['MerchantName','StoreName']
    
    def load_data(self, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                        db_connection_parameters=None):
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            return self.load_data_from_db(db_connection_parameters)
        else:
            return self.load_data_from_local(path_to_file, reading_parameters)
    
    def load_data_from_local(self, path_to_file, reading_parameters):
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns)) != set(self.columns):
            return "Error: can't find needed columns in data"
            
        return df[self.columns]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_transactions(object):
    def __init__(self):
        self.columns = ['Date','CNUM','Amount','MerchantName','MCC','MerchantCity']
    
    def load_data(self, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                        db_connection_parameters=None):
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            return self.load_data_from_db(db_connection_parameters)
        else:
            return self.load_data_from_local(path_to_file, reading_parameters)
    
    def load_data_from_local(self, path_to_file, reading_parameters):
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns)) != set(self.columns):
            return "Error: can't find needed columns in data"
            
        return df[self.columns]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_clients(object):
    def __init__(self):
        self.columns = ['CNUM','Name','Surname','Patronymic','CategoryCode','Gender','Age','Merried',
                        'Email','PhoneNumber','Employer','ResidentType']
    
    def load_data(self, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                        db_connection_parameters=None):
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            return self.load_data_from_db(db_connection_parameters)
        else:
            return self.load_data_from_local(path_to_file, reading_parameters)
    
    def load_data_from_local(self, path_to_file, reading_parameters):
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns)) != set(self.columns):
            return "Error: can't find needed columns in data"
            
        return df[self.columns]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_client_categories(object):
    def __init__(self):
        self.columns = ['Category','CategoryName']
    
    def load_data(self, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                        db_connection_parameters=None):
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            return self.load_data_from_db(db_connection_parameters)
        else:
            return self.load_data_from_local(path_to_file, reading_parameters)
    
    def load_data_from_local(self, path_to_file, reading_parameters):
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns)) != set(self.columns):
            return "Error: can't find needed columns in data"
            
        return df[self.columns]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_client_internet_data(object):
    def __init__(self):
        self.columns = ['CNUM']
    
    def load_data(self, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                        db_connection_parameters=None):
        if path_to_file is None and db_connection_parameters is None:
            return "Error: data source is not set"
        
        if not(path_to_file is None) and not(db_connection_parameters is None):
            return "Error: more than one data source is set"
        
        if path_to_file is None:
            return self.load_data_from_db(db_connection_parameters)
        else:
            return self.load_data_from_local(path_to_file, reading_parameters)
    
    def load_data_from_local(self, path_to_file, reading_parameters):
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns)) != set(self.columns):
            return "Error: can't find needed columns in data"
            
        return df[self.columns]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
        
def create_synthetic_data(path_to_file):
    '''
    in:
    path_to_file: str
    
    out:
    None
    '''
    
    cols = ['MCC','CategoryName']
    pd.DataFrame({c:random.choices(range(1,11), k=10) for c in cols}).to_csv(path_to_file+'mcc.csv', index=False)
    
    cols = ['MerchantName','StoreName']
    pd.DataFrame({c:random.choices(range(1,11), k=10) for c in cols}).to_csv(path_to_file+'stores.csv', index=False)
    
    cols = ['Date','CNUM','Amount','MerchantName','MCC','MerchantCity']
    pd.DataFrame({c:random.choices(range(1,11), k=10) for c in cols}).to_csv(path_to_file+'transactions.csv', index=False)
    
    cols = ['CNUM','Name','Surname','Patronymic','CategoryCode','Gender','Age','Merried',
            'Email','PhoneNumber','Employer','ResidentType']
    pd.DataFrame({c:random.choices(range(1,11), k=10) for c in cols}).to_csv(path_to_file+'clients.csv', index=False)
    
    cols = ['Category','CategoryName']
    pd.DataFrame({c:random.choices(range(1,11), k=10) for c in cols}).to_csv(path_to_file+'client_categories.csv', index=False)
    
    cols = ['CNUM']
    pd.DataFrame({c:random.choices(range(1,11), k=10) for c in cols}).to_csv(path_to_file+'client_internet_data.csv', index=False)
    
    

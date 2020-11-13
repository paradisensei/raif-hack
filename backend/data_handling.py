import numpy as np
import pandas as pd
import sys, os, random, re, datetime, string



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
    dict
    '''
    
    with open(path_to_file, 'r') as f:
        columns = {line.strip().split()[0]:line.strip().split()[1] for line in f.readlines()}
    
    columns = {k:np.int32 if v == 'int' else
                 np.float64 if v == 'float' else 
                 datetime.datetime if v == 'datetime' else 
                 str for k,v in columns.items()}    
    return columns
    
def data_loader(columns, path_to_file=None, reading_parameters={'encoding':'cp1251', 'sep':',', 'extension':'.csv'}, 
                db_connection_parameters=None):
        '''
        in:
        columns: dict(key=column_name, value=dtype)
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
            parse_dates = [k for k,v in columns.items() if v == datetime.datetime]
            if len(parse_dates) == 0:
                parse_dates = False
            columns = {k:str if v == datetime.datetime else v for k,v in columns.items()}
            
            if reading_parameters['extension'] in ['.csv','csv']:
                _ = reading_parameters.pop('extension')
                df = pd.read_csv(path_to_file, dtype=columns, parse_dates=parse_dates, **reading_parameters)

            elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
                _ = reading_parameters.pop('extension')
                df = pd.read_excel(path_to_file, dtype=columns, parse_dates=parse_dates, **reading_parameters)
            
            cols = list(columns.keys())
            if set(list(df.columns)).intersection(set(cols)) != set(cols):
                return "Error: can't find needed columns in data"
            
            return df[cols]

class data_loader_mcc(object):
    def __init__(self):
        self.columns = {'MCC':np.int32,'CategoryName':str}
    
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
            df = pd.read_csv(path_to_file, dtype=self.columns, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, dtype=self.columns, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns.keys())) != set(self.columns.keys()):
            return "Error: can't find needed columns in data"
            
        return df[self.columns.keys()]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_stores(object):
    def __init__(self):
        self.columns = {'MerchantName':str,'StoreName':str}
    
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
            df = pd.read_csv(path_to_file, dtype=self.columns, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, dtype=self.columns, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns.keys())) != set(self.columns.keys()):
            return "Error: can't find needed columns in data"
            
        return df[self.columns.keys()]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_transactions(object):
    def __init__(self):
        self.columns = {'Date':datetime.datetime,'CNUM':np.int32,'Amount':np.float64,'MerchantName':str,'MCC':np.int32,'MerchantCity':str}
    
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
        parse_dates = [k for k,v in self.columns.items() if v == datetime.datetime]
        if len(parse_dates) == 0:
            parse_dates = False
        columns = {k:str if v == datetime.datetime else v for k,v in self.columns.items()}
            
        if reading_parameters['extension'] in ['.csv','csv']:
            _ = reading_parameters.pop('extension')
            df = pd.read_csv(path_to_file, dtype=columns, parse_dates=parse_dates, **reading_parameters)

        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, dtype=columns, parse_dates=parse_dates, **reading_parameters)
            
        cols = list(columns.keys())
        if set(list(df.columns)).intersection(set(cols)) != set(cols):
            return "Error: can't find needed columns in data"
            
        return df[cols]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_clients(object):
    def __init__(self):
        self.columns = {'CNUM':np.int32,'Name':str,'Surname':str,'Patronymic':str,'CategoryCode':np.int32,'Gender':str,'Age':np.int32,'Merried':str,
                        'Email':str,'PhoneNumber':str,'Employer':str,'ResidentType':np.int32}
    
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
            df = pd.read_csv(path_to_file, dtype=self.columns, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, dtype=self.columns, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns.keys())) != set(self.columns.keys()):
            return "Error: can't find needed columns in data"
            
        return df[self.columns.keys()]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_client_categories(object):
    def __init__(self):
        self.columns = {'Category':str,'CategoryName':str}
    
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
            df = pd.read_csv(path_to_file, dtype=self.columns, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, dtype=self.columns, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns.keys())) != set(self.columns.keys()):
            return "Error: can't find needed columns in data"
            
        return df[self.columns.keys()]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
class data_loader_client_internet_data(object):
    def __init__(self):
        self.columns = {'CNUM':np.int32}
    
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
            df = pd.read_csv(path_to_file, dtype=self.columns, **reading_parameters)
            
        elif reading_parameters['extension'] in ['.xls','.xlsx','xls','xlsx']:
            _ = reading_parameters.pop('extension')
            df = pd.read_excel(path_to_file, dtype=self.columns, **reading_parameters)
            
        if set(list(df.columns)).intersection(set(self.columns.keys())) != set(self.columns.keys()):
            return "Error: can't find needed columns in data"
            
        return df[self.columns.keys()]
    
    def load_data_from_db(self, db_connection_parameters):
        pass
    
        
def create_synthetic_data(path_to_file, k=10):
    '''
    in:
    path_to_file: str
    k: int
    
    out:
    None
    '''
    
    cols = {'MCC':np.int32,'CategoryName':str}
    pd.DataFrame(generate_random_dict_with_columns(cols, k)).to_csv(path_to_file+'mcc.csv', index=False)
    
    cols = {'MerchantName':str,'StoreName':str}
    pd.DataFrame(generate_random_dict_with_columns(cols, k)).to_csv(path_to_file+'stores.csv', index=False)
    
    cols = {'Date':datetime.datetime,'CNUM':np.int32,'Amount':np.float64,'MerchantName':str,'MCC':np.int32,'MerchantCity':str}
    pd.DataFrame(generate_random_dict_with_columns(cols, k)).to_csv(path_to_file+'transactions.csv', index=False)
    
    cols = {'CNUM':np.int32,'Name':str,'Surname':str,'Patronymic':str,'CategoryCode':np.int32,'Gender':str,'Age':np.int32,'Merried':str,
            'Email':str,'PhoneNumber':str,'Employer':str,'ResidentType':np.int32}
    pd.DataFrame(generate_random_dict_with_columns(cols, k)).to_csv(path_to_file+'clients.csv', index=False)
    
    cols = {'Category':str,'CategoryName':str}
    pd.DataFrame(generate_random_dict_with_columns(cols, k)).to_csv(path_to_file+'client_categories.csv', index=False)
    
    cols = {'CNUM':np.int32}
    pd.DataFrame(generate_random_dict_with_columns(cols, k)).to_csv(path_to_file+'client_internet_data.csv', index=False)
    
    
def generate_random_dict_with_columns(cols, n):
    '''
    in:
    cols: dict(key=column_name, value=str)
    n = int
    
    out:
    dict(key=column_name, value=dtype)
    '''

    random_dict = {k:random.choices(range(1,11), k=n) if v == np.int32 else
                     np.random.uniform(low=1, high=11, size=(n,)) if v == np.float64 else    
                     [generate_random_datetime() for i in range(n)] if v == datetime.datetime else 
                     random.choices(string.ascii_letters, k=n) for k,v in cols.items()
                  }
    
    return random_dict
    
def generate_random_datetime(start_date=datetime.datetime(2020, 1, 1), end_date=datetime.datetime(2020, 10, 1)):
    '''
    in:
    start_date: datetime.datetime
    start_date: datetime.datetime
    
    out:
    datetime.datetime
    '''
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    
    return random_date
    
    
    
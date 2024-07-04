# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:49:27 2024

@author: Hogan
"""

import sqlite3
import pandas as pd
import numpy as np
import sqlalchemy as sql
import datetime as dt
from sqlite3 import Error


class SQLite:
    def __init__(self):
        return
    
    def connect(self, path):
        try:
            self.connection = sqlite3.connect(path)    
        except Exception as e:
            print(e)
        return
    
    def insert_df_to_table(self, df, table_name, modifiedat=True, if_exists='append', delete_whereclause='1=1'):
        
        if modifiedat:
            df['ModifiedAt'] = dt.datetime.now()
        cursor = self.connection.cursor()
        cursor.execute("BEGIN")
        try:
            # Execute delete clause
            table_name_quote = '"'+table_name+'"'
            cursor.execute(f'delete FROM {table_name_quote} where {delete_whereclause}')
            df.to_sql(table_name, con=self.connection, if_exists=if_exists, chunksize=5000, index=False)
            
        except Exception as e:
            cursor.execute("ROLLBACK")
            raise Exception(e)
        else:
            pass
        
        return
    
    def get_data_from_table(self, table_name, schema_name=None, columns=None, select_whereclause='1=1'):
        try:
            # Execute delete clause
            table_name_quote = '"'+table_name+'"'
            res = pd.read_sql(f'SELECT * FROM {table_name_quote} where {select_whereclause}', self.connection)
            return res
        except:
            raise ValueError('Something was wrong...')
    

    
if __name__ =="__main__":
    
    test = SQLite()
    test.connect(path='D://Box//Data//prism_local//econdata.db')

    testdata = pd.DataFrame(columns=['ID','Date','Value'])
    testdata.loc[0] = ['Test', dt.date(2024,1,1),10.22343234]
    
    test.insert_df_to_table(df=testdata, table_name='econdata', if_exists='replace', delete_whereclause='"ID"=\'Test\'')
    test1 = test.get_data_from_table(table_name='econdata')  
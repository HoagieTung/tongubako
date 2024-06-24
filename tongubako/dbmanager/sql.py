# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 11:51:51 2024

@author: Hogan
"""

import sqlite3
import pandas as pd
import numpy as np
import sqlalchemy as sql
import datetime as dt
from sqlite3 import Error

class SQL:
    def __init__(self, dbtype='POSTGRE'):
        self.dbtype = dbtype
        return
    
    def connect(self, user, password, host, port=None, dbname=None, fast_executemany=False, echo=False, schema=None, connection_string=None):
        if connection_string is not None:
            self.uri = connection_string
        elif self.dbtype.upper() in ['POSTGRE','POSTGRESQL']:
            self.uri = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(user=user, password=password, host=host, port=port, dbname=dbname)
        elif self.dbtype.upper() in ['MYSQL']:
            pass
        
        self.engine = sql.create_engine(self.uri, echo=echo)

        return
    
    def execute_query(self, query):
        res = self.connection.execute(query)
        return res
    
    def insert_df_to_table(self, df, table_name, schema_name=None, modifiedat=True, if_exists='append', delete_whereclause='1=1'):
        
        if modifiedat:
            df['ModifiedAt'] = dt.datetime.now()
        conn = self.engine.connect()
        t = conn.begin()
        try:
            # Execute delete clause
            table_name_quote = '"'+table_name+'"'
            if schema_name is not None:
                schema_name_quote = '"'+schema_name+'"'
                conn.execute(sql.text(f'delete FROM {schema_name_quote}.{table_name_quote} where {delete_whereclause}'))
            else:
                conn.execute(sql.text(f'delete FROM {table_name_quote} where {delete_whereclause}'))
                
            df.to_sql(table_name, con=conn, if_exists=if_exists, schema=schema_name, chunksize=5000, index=False)
            
        except Exception as e:
            t.rollback()
            raise Exception(e)
        else:
            t.commit()

        return
    
    def get_data_from_table(self, table_name, schema_name=None, columns=None, select_whereclause='1=1'):
        conn = self.engine.connect()
        try:
            # Execute delete clause
            table_name_quote = '"'+table_name+'"'
            if schema_name is not None:
                schema_name_quote = '"'+schema_name+'"'
                res = pd.read_sql(f'SELECT * FROM {schema_name_quote}.{table_name_quote} where {select_whereclause}', conn)
            else:
                res = pd.read_sql(f'SELECT * FROM {table_name_quote} where {select_whereclause}', conn)
            return res
        except:
            raise ValueError('Something was wrong...')
    
    def conditional_statement(self, conditions):
        if not isinstance(conditions, dict):
            raise TypeError('conditions must be in dict format')
        condition_list = []
        for key, item in conditions.items():
            c = f'"{key}"='
        return
            
    
if __name__ =="__main__":
    
    test = SQL()
    test.connect(user='admin', password='83I35jM8pAWSo6BekIa8v805',host='mistakenly-distinct-anchovy.a1.pgedge.io', dbname='htdb',port='5432')

    testdata = pd.DataFrame(columns=['ID','Date','Value'])
    testdata.loc[0] = ['Test', dt.date(2024,1,1),10.789]
    
    test.insert_df_to_table(df=testdata, table_name='econdata', schema_name='datanexus', if_exists='replace', delete_whereclause='"ID"=\'Test\'')
    test1 = test.get_data_from_table(table_name='econdata', schema_name='datanexus')  
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 14:19:08 2024

@author: homoi
"""

import pandas as pd
import numpy as np

class SQL():
    def __init__(self, schema, dbtype='postgres'):
        self.dbtype = dbtype
        self.schema = schema
    
    
    def connect(self):
        if self.dbtype.upper() in ['POSTGRES','POSTGRE']:
            pass
        
        return
    
    
    def insert_dataframe_to_table(self, df, table, delete_clause=None):
        
        return
        
    def generate_delete_clause(self, columns):
        if isinstance(columns, str):
            columns = [columns]
        clause = 'WHERE '
        for col in columns:  
            clause += '\"{col}\"={}'
        return
        
        
        
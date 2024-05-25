# -*- coding: utf-8 -*-
"""
Created on Sat May 25 14:19:08 2024

@author: homoi
"""

class SQL():
    def __init__(self, schema, dbtype='postgres'):
        self.dbtype = dbtype
        self.schema = schema
    
    
    def connect(self):
        
        return
    
    
    def insert_dataframe_to_table(self, df, table, delete_clause=None):
        
        return
        
    def generate_delete_clause(self, columns):
        if isinstance(columns, str):
            columns = [columns]
       
        return
        
        
        
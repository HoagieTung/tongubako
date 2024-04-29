# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 22:26:33 2024

@author: Hogan
"""

import pandas as pd
import numpy as np

class DEA():
    def __init__(self, X, Y):
        "rows are attributes, columns are units"
        if len(X.columns)!=len(Y.columns):
            raise ValueError("Error: Number of units inconsistent")
            
        self.X = X
        self.Y = Y
        
        self.n_units = len(X.columns)
        self.n_inputs = len(X.index)
        self.n_outputs = len(Y.index)
        
        self._i = range(self.n_units)
        self._j = range(self.n_inputs)
        self._k = range(self.n_outputs)
        self.efficiency = pd.DataFrame(data=np.nan, index=range(self.n_units), columns=['DMU','Efficiency','Theta'])
        self._lambda = pd.DataFrame(data=np.nan, index=self._i, columns=X.columns)
        self._s_plus = pd.DataFrame(data=np.nan, index=self._k, columns=X.columns)
        self._lambda = pd.DataFrame(data=np.nan, index=self._j, columns=X.columns)
        self.models = {}
    
    def regulate_data_format(self, data):
        
        if isinstance(data, pd.DataFrame):
            pass    
        elif isinstance(data, np.array):
            data = pd.DataFrame(data)
        elif isinstance(data, np.mat):
            data = pd.DataFrame(data)
        
        if len(data.columns) < 2 * len(data.columns):
            raise ValueError("Number of units must be larger than 2x number of attributes")
    
    
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:56:44 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt
import requests
from tongubako.utils import guess_frequency

from . import fetch_data, process_data

class CNNBS():
    def __init__(self, proxies=None):
        self.proxies = proxies
        self.data_list = pd.read_excel('tongubako//cnnbs//catalog.xlsx','data_list')
        self.data_dictionary = self.data_list.set_index('SID').to_dict(orient='index')
        return
    
    def get_series_data(self, sid, bound_type='last', start_date=None, end_date=None, details=True):
        
        return
    


# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:48:42 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
from tongubako.utils import guess_frequency


class DBnomics():
    def __init__(self, apikey, proxies=None):
        self.apikey = apikey
        self.proxies = proxies
        return

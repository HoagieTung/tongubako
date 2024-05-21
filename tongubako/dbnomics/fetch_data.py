# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:51:58 2024

@author: Hogan
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta, date
import requests
import json 



def fetch_series(self, sid):
    url = 'https://api.db.nomics.world/v22/series/{sid}?facets=false&observations=True&metadata=true&format=json&align_periods=true&limit=1000&offset=0'.format(sid=sid)
    x = requests.get(url)
    data = json.loads(x.content)
    return data
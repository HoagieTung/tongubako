# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 23:06:12 2024

@author: homoi
"""
import time
from functools import lru_cache
from typing import Union, Literal, List, Dict
import numpy as np
import pandas as pd
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

db_code = {"M": "hgyd", "Q": "hgjd", "A": "hgnd"}

def get_child_indicators(category_id: str, freq: str, proxies=None) -> List[Dict]:
    url = "https://data.stats.gov.cn/english/easyquery.htm"
    params = {"id": category_id, "dbcode": db_code[freq], "wdcode": "zb", "m": "getTree"}
    r = requests.post(url, params=params, verify=False, allow_redirects=True, proxies=proxies)
    data_json = r.json()
    return pd.DataFrame(data_json)

test = get_child_indicators('A0102','M')


def fetch_category_data(category_id, freq='M', period="1995-", proxies=None):
    url = "https://data.stats.gov.cn/english/easyquery.htm"
    params = {
        "m": "QueryData",
        "dbcode": db_code[freq],
        "rowcode": "zb",
        "colcode": "sj",
        "wds": "[]",
        "dfwds": '[{"wdcode":"zb","valuecode":"%s"}, '
        '{"wdcode":"sj","valuecode":"%s"}]' % (category_id, period),
        "k1": str(time.time_ns())[:13],
    }
    r = requests.get(url, params=params, verify=False, allow_redirects=True)
    data_json = r.json()

    return data_json


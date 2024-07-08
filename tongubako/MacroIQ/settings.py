# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:49:09 2024

@author: Hogan
"""

from . import fetch_data
import foo


FUNCTIONS = {
        'CNM0MS': fetch_data.fetch_cn_money_supply,
        'CNM1MS': fetch_data.fetch_cn_money_supply,
        'CNM2MS': fetch_data.fetch_cn_money_supply,
        }
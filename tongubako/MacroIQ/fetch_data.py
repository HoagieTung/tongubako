# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 22:24:13 2024

@author: Hogan
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import time
import requests
import json
import warnings

warnings.filterwarnings(action="ignore", category=FutureWarning)

def fetch_cn_money_supply(sid, units='yoy', proxies=None):
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "columns":"REPORT_DATE,TIME,BASIC_CURRENCY,BASIC_CURRENCY_SAME,BASIC_CURRENCY_SEQUENTIAL,CURRENCY,CURRENCY_SAME,CURRENCY_SEQUENTIAL,FREE_CASH,FREE_CASH_SAME,FREE_CASH_SEQUENTIAL",
        "reportName": "RPT_ECONOMY_CURRENCY_SUPPLY",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "1",
        }
    
    r = requests.get(url, params=params, proxies=proxies)
    data_json = r.json()

    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = ["date","month","M2","M2_yoy","M2_mom","M1","M1_yoy","M1_mom","M0","M0_yoy","M0_mom"]
    temp_df.index = temp_df['date'].apply(lambda x: dt.datetime.strptime(x.split(' ')[0],'%Y-%m-%d').date()).values
    temp_df = temp_df.drop(['date','month'], axis=1)
    for i in range(1, len(temp_df.columns)):   
        temp_df.iloc[:,i] = pd.to_numeric(temp_df.iloc[:,i], errors="coerce")
    
    if sid.upper() in ['CNM0MS','CNM1MS','CNM2MS']:
        money = sid[2:4].upper()
        if units.upper() in ['YOY','PC1','DEFAULT']:
            output = temp_df['{}_yoy'.format(money)]
        elif units.upper() in ['MOM','PCT']:
            output = temp_df['{}_mom'.format(money)]
        elif units.upper() in ['LEVEL','LIN']:
            output = temp_df['{}'.format(money)]
    
    return output


def fetch_cn_industrial_production(sid, units='yoy', proxies=None):
    if units.upper() not in ['YOY','YTD']:
        raise ValueError('China industrial production data must be yoy and ytd.')
        
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "columns":"REPORT_DATE,TIME,BASIC_CURRENCY,BASIC_CURRENCY_SAME,BASIC_CURRENCY_SEQUENTIAL,CURRENCY,CURRENCY_SAME,CURRENCY_SEQUENTIAL,FREE_CASH,FREE_CASH_SAME,FREE_CASH_SEQUENTIAL",
        "reportName": "RPT_ECONOMY_CURRENCY_SUPPLY",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "1",
        }
    
    r = requests.get(url, params=params, proxies=proxies)
    data_json = r.json()

    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = ["date","month","M2","M2_yoy","M2_mom","M1","M1_yoy","M1_mom","M0","M0_yoy","M0_mom"]
    temp_df.index = temp_df['date'].apply(lambda x: dt.datetime.strptime(x.split(' ')[0],'%Y-%m-%d').date()).values
    temp_df = temp_df.drop(['date','month'], axis=1)
    for i in range(1, len(temp_df.columns)):   
        temp_df.iloc[:,i] = pd.to_numeric(temp_df.iloc[:,i], errors="coerce")
    
    if sid.upper() in ['CNM0MS','CNM1MS','CNM2MS']:
        money = sid[2:4].upper()
        if units.upper() in ['YOY','PC1','DEFAULT']:
            output = temp_df['{}_yoy'.format(money)]
        elif units.upper() in ['MOM','PCT']:
            output = temp_df['{}_mom'.format(money)]
        elif units.upper() in ['LEVEL','LIN']:
            output = temp_df['{}'.format(money)]
    
    return output


def jin10_data(symbol, params):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "x-csrf-token",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "58",
        "_": str(int(round(time.time() * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                dt.datetime.strptime(last_date_str, "%Y-%m-%d")
                - dt.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
    ]
    big_df["商品"] = symbol
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"], errors="coerce")
    big_df["预测值"] = pd.to_numeric(big_df["预测值"], errors="coerce")
    big_df["前值"] = pd.to_numeric(big_df["前值"], errors="coerce")
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return


if __name__ =="__main__":
    
    test1 = fetch_cn_money_supply(sid='CNM1MS', units='yoy', proxies=None)
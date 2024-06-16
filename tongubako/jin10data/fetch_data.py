# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 16:41:51 2024

@author: homoi
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import requests
import json

#from . import settings


def get( proxies=None):
    x = requests.get("https://datacenter-api.jin10.com/reports/list_v2", proxies=proxies)
    data = json.loads(x.content)
    return data

def __macro_usa_base_func(symbol: str, params: dict) -> pd.DataFrame:
    """
    金十数据中心-经济指标-美国-基础函数
    https://datacenter.jin10.com/economic
    :return: 美国经济指标数据
    :rtype: pandas.DataFrame
    """
    import warnings

    warnings.filterwarnings(action="ignore", category=FutureWarning)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "x-csrf-token",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = params
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
    return big_df


# 东方财富-美国-未决房屋销售月率
def macro_usa_phs() -> pd.DataFrame:
    """
    东方财富-经济数据一览-美国-未决房屋销售月率
    https://data.eastmoney.com/cjsj/foreign_0_5.html
    :return: 未决房屋销售月率
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_ECONOMICVALUE_USA",
        "columns": "ALL",
        "filter": '(INDICATOR_ID="EMG00342249")',
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1669047266881",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "-",
        "-",
        "时间",
        "-",
        "发布日期",
        "现值",
        "前值",
    ]
    temp_df = temp_df[
        [
            "时间",
            "前值",
            "现值",
            "发布日期",
        ]
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
    temp_df["现值"] = pd.to_numeric(temp_df["现值"], errors="coerce")
    temp_df["发布日期"] = pd.to_datetime(temp_df["发布日期"], errors="coerce").dt.date
    return temp_df


# 东方财富-经济指标-美国-物价水平-美国核心CPI月率报告
def macro_usa_cpi_yoy() -> pd.DataFrame:
    """
    东方财富-经济数据一览-美国-CPI年率, 数据区间从 2008-至今
    https://data.eastmoney.com/cjsj/foreign_0_12.html
    :return: 美国 CPI 年率报告
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_ECONOMICVALUE_USA",
        "columns": "ALL",
        "filter": '(INDICATOR_ID="EMG00000733")',
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "_": "1689320600161",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    data_list = data_json["result"]["data"]
    temp_df = pd.DataFrame(
        data_list, columns=["REPORT_DATE", "PUBLISH_DATE", "VALUE", "PRE_VALUE"]
    )
    temp_df.columns = [
        "时间",
        "发布日期",
        "现值",
        "前值",
    ]
    temp_df["时间"] = pd.to_datetime(temp_df["时间"], errors="coerce").dt.date
    temp_df["发布日期"] = pd.to_datetime(temp_df["发布日期"], errors="coerce").dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
    temp_df["现值"] = pd.to_numeric(temp_df["现值"], errors="coerce")
    temp_df.sort_values(by=["时间"], inplace=True, ignore_index=True)
    return temp_df


if __name__ =="__main__":
    
    test1 = get()

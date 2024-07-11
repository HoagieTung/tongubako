# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 23:06:12 2024

@author: homoi
"""
import time
from functools import lru_cache
from typing import Union, Literal, List, Dict

import jsonpath as jp
import numpy as np
import pandas as pd
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# 忽略InsecureRequestWarning警告
urllib3.disable_warnings(InsecureRequestWarning)

db_code = {"M": "hgyd", "Q": "hgjd", "A": "hgnd"}

def get_child_indicators(category_id: str, freq: str, proxies=None) -> List[Dict]:
    url = "https://data.stats.gov.cn/english/easyquery.htm"
    params = {"id": category_id, "dbcode": db_code[freq], "wdcode": "zb", "m": "getTree"}
    r = requests.post(url, params=params, verify=False, allow_redirects=True, proxies=proxies)
    data_json = r.json()
    return pd.DataFrame(data_json)

test = get_child_indicators('zb','M')

def _get_nbs_wds_tree(idcode: str, dbcode: str, rowcode: str) -> List[Dict]:
    """
    获取地区数据的可选指标目录树
    :param idcode: 指标编码
    :param dbcode: 库编码
    :param rowcode: 值为zb是返回地区的编码，值为reg时返回可选指标的编码
    :return:  json数据
    """
    url = "https://data.stats.gov.cn/english/easyquery.htm"
    params = {
        "m": "getOtherWds",
        "dbcode": dbcode,
        "rowcode": rowcode,
        "colcode": "sj",
        "wds": '[{"wdcode":"zb","valuecode":"%s"}]' % idcode,
        "k1": str(time.time_ns())[:13],
    }
    r = requests.post(url, params=params, verify=False, allow_redirects=True)
    data_json = r.json()
    data_json = data_json["returndata"][0]["nodes"]
    return data_json




def fetch_data(sid, freq='M', period="1990-", proxies=None):
    url = "https://data.stats.gov.cn/english/easyquery.htm"
    params = {
        "m": "QueryData",
        "dbcode": db_code[freq],
        "rowcode": "zb",
        "colcode": "sj",
        "wds": "[]",
        "dfwds": '[{"wdcode":"zb","valuecode":"%s"}, '
        '{"wdcode":"sj","valuecode":"%s"}]' % (sid, period),
        "k1": str(time.time_ns())[:13],
    }
    r = requests.get(url, params=params, verify=False, allow_redirects=True)
    data_json = r.json()

    # 整理为dataframe
    temp_df = pd.DataFrame(data_json["returndata"]["datanodes"])
    temp_df["data"] = temp_df["data"].apply(
        lambda x: x["data"] if x["hasdata"] else None
    )
    return

def macro_china_nbs_nation(
    kind: Literal["M", "Q", "A"], path: str, period: str = "1990-"
) -> pd.DataFrame:
    """
    国家统计局全国数据通用接口
    https://data.stats.gov.cn/easyquery.htm
    :param kind: 数据类别
    :param path: 数据路径
    :param period: 时间区间，例如'LAST10', '2016-2023', '2016-'等
    :return: 国家统计局统计数据
    :rtype: pandas.DataFrame
    """
    # 获取dbcode
    dbcode = kind_code[kind]

    # 获取最终id
    parent_tree = get_nbs_tree("zb", dbcode)
    path_split = path.replace(" ", "").split(">")
    indicator_id = _get_code_from_nbs_tree(parent_tree, path_split[0])
    path_split.pop(0)
    while path_split:
        temp_tree = _get_nbs_tree(indicator_id, dbcode)
        indicator_id = _get_code_from_nbs_tree(temp_tree, path_split[0])
        path_split.pop(0)

    # 请求数据
    url = "https://data.stats.gov.cn/easyquery.htm"
    params = {
        "m": "QueryData",
        "dbcode": dbcode,
        "rowcode": "zb",
        "colcode": "sj",
        "wds": "[]",
        "dfwds": '[{"wdcode":"zb","valuecode":"%s"}, '
        '{"wdcode":"sj","valuecode":"%s"}]' % (indicator_id, period),
        "k1": str(time.time_ns())[:13],
    }
    r = requests.get(url, params=params, verify=False, allow_redirects=True)
    data_json = r.json()

    # 整理为dataframe
    temp_df = pd.DataFrame(data_json["returndata"]["datanodes"])
    temp_df["data"] = temp_df["data"].apply(
        lambda x: x["data"] if x["hasdata"] else None
    )

    wdnodes = data_json["returndata"]["wdnodes"]
    wn_df_list = []
    for wn in wdnodes:
        wn_df_list.append(
            pd.DataFrame(wn["nodes"])
            .assign(
                funit=lambda df: df["unit"].apply(lambda x: "(" + x + ")" if x else x)
            )
            .assign(fname=lambda df: df["cname"] + df["funit"]),
        )

    row_name, column_name = (
        wn_df_list[0]["fname"],
        wn_df_list[1]["fname"],
    )

    data_ndarray = np.reshape(temp_df["data"], (len(row_name), len(column_name)))
    data_df = pd.DataFrame(data=data_ndarray, columns=column_name, index=row_name)
    data_df.index.name = None
    data_df.columns.name = None

    return data_df

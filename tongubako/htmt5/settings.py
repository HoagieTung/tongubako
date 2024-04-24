# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 23:40:41 2024

@author: Hogan
"""
import MetaTrader5

frequency={
    'M1': MetaTrader5.TIMEFRAME_M1,
    'M2': MetaTrader5.TIMEFRAME_M2,
    'M3': MetaTrader5.TIMEFRAME_M3,
    'M5': MetaTrader5.TIMEFRAME_M5,
    'M10': MetaTrader5.TIMEFRAME_M10,
    'M15': MetaTrader5.TIMEFRAME_M15,
    'M20': MetaTrader5.TIMEFRAME_M20,
    'M30': MetaTrader5.TIMEFRAME_M30,
    'H1': MetaTrader5.TIMEFRAME_H1,
    'H2': MetaTrader5.TIMEFRAME_H2,
    'H4': MetaTrader5.TIMEFRAME_H4,
    'H6': MetaTrader5.TIMEFRAME_H6,
    'H8': MetaTrader5.TIMEFRAME_H8,
    'H12': MetaTrader5.TIMEFRAME_H12,
    'D1': MetaTrader5.TIMEFRAME_D1,
    }

ochl_frequency={
    'M30': 'M1',
    'H1': 'M2',
    'H2': 'M10',
    'H4': 'M10',
    'H6': 'M20',
    'H8': 'M30',
    'H12': 'M30',
    'D1': 'M15',
    }

order_type={
    -1: MetaTrader5.ORDER_TYPE_SELL,
    1: MetaTrader5.ORDER_TYPE_BUY,
    }

filling_type={
    1: MetaTrader5.ORDER_FILLING_FOK,
    2: MetaTrader5.ORDER_FILLING_IOC,
    }

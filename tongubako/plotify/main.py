# -*- coding: utf-8 -*-
"""
Created on Sun May 12 11:29:04 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt
from tongubako.utils import guess_frequency
import matplotlib.pyplot as plt 


class Constructor():
    __slots__ = [
        "x",
        "y",
        "chart_type",
        "style",
        "figsize",
        "color",
        "x_title",
        "y_title",
        "z_title",
        "chart_title",
        "axis",
        "labels",
        "axis_range",
    ]
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x, self.y = None, None
        self.chart_type = None
        self.style = None
        self.figsize = (16,10)
        self.color = {}
        self.x_title, self.y_title, self.z_title, self.chart_title = None, None, None, None
        self.axis = {}
        self.labels = {}
        self.axis_range = {}
    
    def regulate_data(self, x, y):
        if isinstance(y, list):
            y = pd.concat(y, axis=1)
        elif isinstance(y, pd.Series):
            y = y.to_frame()
        if len(x) != len(y.index):
            raise ValueError("x and y must have the same length")
        return x, y
    
    def set_type(self, chart_type_mapping):
        if isinstance(chart_type_mapping, str):
            self.chart_type = chart_type_mapping
        elif isinstance(chart_type_mapping, list):
            for i in range(len(self.y.columns)):
                self.chart_type[self.y.columns[i]] = chart_type_mapping[i]
        elif isinstance(chart_type_mapping, dict):
            self.chart_type = chart_type_mapping
    
    def add_data(self, x, y):
        self.x, self.y = self.regulate_data(x, y)
    
    def add_labels(self, labels_mapping=None):
        if self.y is None:
            raise ValueError("Add data before adding labels, use the add_data function")
        if labels_mapping is None:
            for i in range(len(self.y.columns)):
                if self.y.columns[i] not in labels_mapping.keys():
                    self.labels[self.y.columns[i]] = self.y.columns[i]
        elif isinstance(labels_mapping, list):
            for i in range(len(self.y.columns)):
                self.labels[self.y.columns[i]] = labels_mapping[i]
        elif isinstance(labels_mapping, dict):
            self.labels = labels_mapping
            for i in range(len(self.y.columns)):
                if self.y.columns[i] not in labels_mapping.keys():
                    self.labels[self.y.columns[i]] = self.y.columns[i]

    def set_axis(self, axis_mapping):
        if not bool(self.labels):
            raise ValueError("Add labels before setting axis, use the add_labels function")
        if isinstance(axis_mapping, list):
            for i in range(len(self.y.columns)):
                self.axis[self.y.columns[i]] = axis_mapping[i]
        elif isinstance(axis_mapping, dict):
            for i in range(len(self.y.columns)):
                if self.y.columns[i] not in axis_mapping.keys():
                    axis_mapping[self.y.columns[i]] = self.y.columns[i]
    
    def set_axis_range(self, axis_range_mapping):
        
        
        
    


if __name__ == '__main__':
    test = Constructor()
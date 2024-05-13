# -*- coding: utf-8 -*-
"""
Created on Sun May 12 17:55:45 2024

@author: Hogan
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from .util import move_spine, make_patch_spines_invisible

colors = ['k','r','b']

def line(constructor, **kwargs):
    plt.style.use('default')
    splines = {}
    plots = {}
    fig, splines['L1'] = plt.subplots(figsize=constructor.figsize, layout='constrained')
    splines['L1'].patch.set_visible(False)
    splines['L1'].spines['left'].set_visible(True)
    
    
    for k in list(constructor.axis.values()):
        if k == 'L1':
            continue
        splines[k] = splines['L1'].twinx()
    
    for k in range(len(constructor.y.columns)):
        name = constructor.y.columns[k]
        label = constructor.labels[name]
        axis = constructor.axis[name]

        plots[name] = splines[axis].plot(constructor.x, constructor.y.iloc[:,k], color=colors[k], label=label)
        splines[axis].set_ylabel(label)
        splines[axis].yaxis.label.set_color(plots[name][0].get_color())
        
        if axis == 'R2':
        
            splines[axis].spines['right'].set_position(('outward', 60))
            splines[axis].set_frame_on(True)
            splines[axis].patch.set_visible(False)
            splines[axis].spines['right'].set_visible(True)
            splines[axis].get_yaxis().set_tick_params(direction='out')
           
    
    fig.show()
    
    return
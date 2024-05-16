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

def line(constructor, show=False, **kwargs):
    plt.style.use('default')
    axes = {}
    plots = {}
    fig, axes['L1'] = plt.subplots(figsize=constructor.figsize, layout='constrained')
    axes['L1'].patch.set_visible(False)
    axes['L1'].spines['left'].set_visible(True)
    
    
    for k in list(constructor.axis.values()):
        if k == 'L1':
            continue
        axes[k] = axes['L1'].twinx()
    
    for k in range(len(constructor.y.columns)):
        name = constructor.y.columns[k]
        label = constructor.labels[name]
        axis = constructor.axis[name]

        plots[name] = axes[axis].plot(constructor.x, constructor.y.iloc[:,k], color=colors[k], label=label)
        axes[axis].set_ylabel(label)
        axes[axis].yaxis.label.set_color(plots[name][0].get_color())
        
        if 'R' in axis.upper():
            n = int(axis.replace('R','').replace('r','')) - 1
            axes[axis].spines['right'].set_position(('outward', constructor.axis_shift*n))
            axes[axis].patch.set_visible(False)
            axes[axis].spines['right'].set_visible(True)
            axes[axis].get_yaxis().set_tick_params(direction='out')
        
        elif 'L' in axis.upper():
            n = int(axis.replace('L','').replace('l','')) - 1
            axes[axis].spines['left'].set_position(('outward', constructor.axis_shift*n))
            axes[axis].patch.set_visible(False)
            axes[axis].spines['left'].set_visible(True)
            axes[axis].yaxis.set_label_position('left')
            axes[axis].yaxis.set_ticks_position('left')
            axes[axis].get_yaxis().set_tick_params(direction='out')
    
        plt.legend(loc='best')
    
    for key, item in constructor.axis_range.items():
        if item is not None:
            axes[key].set_ylim(item[0], item[1])
    
    if show:
        fig.show()

    return fig
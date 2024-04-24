# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 21:04:04 2024

@author: Hogan
"""

from datetime import datetime, timedelta, time, date
import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AR


def kalman_filter_update(x, P, A, H, z, R, Q, B=None, u=None):
    # x_k = Ax_{k-1} +Bu_k + w
    # z = Hx + v
    # w ~ N(0, Q), Q is the process noise covariance
    # v ~ N(0, R), R is the observation noise
    x_priori = A.dot(x) + B.dot(u) if B is not None and u is not None else A.dot(x)
    P_priori = A.dot(P).dot(A.T) + Q
    
    K = P_priori.dot(H.T).dot(np.linalg.inv(H.dot(P_priori).dot(H.T)+R))
    
    x_posteriori = x_priori + K*(z-H.dot(x_priori))
    P_posteriori = P_priori - K*H.dot(P_priori)
    
    return x_posteriori, P_posteriori


class KalmanFilter:
    def __init__(self):
        return
    
    def initial_estimate(self, data):
        # x_k = A + B*x_{k-1} +C*e_k
        # y_k = x_k + D*w_k
        state_equation = AR(data).fit(1)
        A,B = state_equation.params
        C = state_equation.resid.std()
        D = (data - A/(1-B)).std()
        return A, B, C, D
    
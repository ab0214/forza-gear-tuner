# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:32:57 2023

@author: AB0214
"""

import numpy as np
from scipy import stats

class PowerCurve:
    def __init__(self, telemetry):
        # Filter irrelevant data
        powercurve = telemetry.loc[
            (telemetry['Throttle'] == 255) &
            (telemetry['Clutch'] == 0) &
            (telemetry['Torque'] > 0),
            ['RPM', 'Torque', 'Power']]
        
        # Filter NA and outliers
        powercurve.dropna(inplace=True)
        z = np.abs(stats.zscore(powercurve))
        not_outlier = (z < 4)
        powercurve = powercurve[not_outlier]
        
        # Sort
        powercurve = powercurve.sort_values(by='RPM')

        # Filter noisy data
        window_size = 15  # Adjust the window size as per your preference
        for name, values in powercurve.items():
            smoothed = values.rolling(window_size).max()
            powercurve[name] = smoothed
        
        # Convert watts to kilowatts
        #powercurve['Power'] = powercurve['Power'].apply(lambda x: x/1000)
        
        # TODO: resample and interpolate
        
        self.data = powercurve
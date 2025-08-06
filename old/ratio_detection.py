# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 00:11:43 2023

@author: AB0214
"""

#import convert
import math
import pandas as pd
import numpy as np
from scipy import stats
from enums import DriveTrainType
from pint import UnitRegistry

ureg = UnitRegistry()
    
def get_output_rads(telemetry_frame):
    match telemetry_frame['Drivetrain']:
        
        case DriveTrainType.FWD:
            return (
                telemetry_frame['WheelSpeedFL'] +
                telemetry_frame['WheelSpeedFR']
                )/2
            
        case DriveTrainType.RWD:
            return (
                telemetry_frame['WheelSpeedRL'] +
                telemetry_frame['WheelSpeedRR']
                )/2
            
        case DriveTrainType.AWD:
            return (
                telemetry_frame['WheelSpeedFL'] +
                telemetry_frame['WheelSpeedFR'] +
                telemetry_frame['WheelSpeedRL'] +
                telemetry_frame['WheelSpeedRR']
                )/4


def get_ratio(telemetry_frame):
    input_rpm = telemetry_frame['RPM'] * ureg.rpm
    output_rads = get_output_rads(telemetry_frame) * (ureg.radian / ureg.second)
    output_rpm = output_rads.to(ureg.rpm)
    ratio = (input_rpm / output_rpm)
    return ratio.magnitude


def detect_ratio(telemetry, gear):
    filtered = telemetry[
        (telemetry['Gear'] == gear) &
        (telemetry['Clutch'] == 0) &
        (telemetry['WheelSpeedFL'] > 0) &
        (telemetry['WheelSpeedFR'] > 0) &
        (telemetry['WheelSpeedRL'] > 0) &
        (telemetry['WheelSpeedRR'] > 0) &
        (telemetry['Speed'] > 0) & 
        (telemetry['RPM'] > telemetry['IdleRPM'] * 1.5)]
    
    ratios = filtered.apply(get_ratio, axis=1)
    
    ratios.dropna(inplace=True)
    z = np.abs(stats.zscore(ratios))
    ratios = ratios[(z < 1)]
    
    return ratios.mean()
    
    
def detect_ratios(telemetry):
    gear_count = telemetry['Gear'].max()
    gear_numbers = range(1, gear_count + 1, 1)
    gear_ratios = pd.Series(index=gear_numbers)
    for gear, ratio in gear_ratios.items():
        gear_ratios[gear] = detect_ratio(telemetry, gear)
    return gear_ratios


def detect_wheel_circumference(telemetry):
    filtered = telemetry[
        (telemetry['WheelSpeedFL'] > 0) &
        (telemetry['WheelSpeedFR'] > 0) &
        (telemetry['WheelSpeedRL'] > 0) &
        (telemetry['WheelSpeedRR'] > 0) &
        (telemetry['Speed'] > 0) &
        (telemetry['Throttle'] == 0) &
        (telemetry['Brake'] == 0)]
    
    cs = filtered.apply(get_wheel_circumference, axis=1)
    cs.dropna(inplace=True)
    z = np.abs(stats.zscore(cs))
    cs = cs[(z < 1)]
    
    return cs.mean()

    
def get_wheel_circumference(telemetry_frame):
    wheel_rads = get_output_rads(telemetry_frame)
    #wheel_rps = wheel_rads / math.tau
    circumference = telemetry_frame['Speed'] / (wheel_rads / math.tau)
    return circumference
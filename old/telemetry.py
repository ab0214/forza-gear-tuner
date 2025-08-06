# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 00:10:39 2023

@author: AB0214
"""


import struct
import pandas as pd



field_names = [
    'IsRaceOn',
    'TimestampMS', # can overflow to 0
    'MaxRPM', 'IdleRPM', 'RPM', # engine max, idle, and current rpm
    'AccelX', 'AccelY', 'AccelZ',       # m/s^2?, car's right, up, forward
    'LinVelX', 'LinVelY', 'LinVelZ', # m/s?, car's right, up, forward
    'AngVelX', 'AngVelY', 'AngVelZ', # rad/s?, car's right, up, forward
    'Yaw', 'Pitch', 'Roll', # units?
    'SuspNormFL', 'SuspNormFR', # 0 = fully extended, 
    'SuspNormRL', 'SuspNormRR', # 1 = fully compressed.
    'SlipRatioFL', 'SlipRatioFR', # 0 = max grip, 1 = min grip
    'SlipRatioRL', 'SlipRatioRR', # longtitudinal??
    'WheelSpeedFL', 'WheelSpeedFR', # rad/s
    'WheelSpeedRL', 'WheelSpeedRR', # rad/s
    'OnRumbleStripFL', 'OnRumbleStripFR', 
    'OnRumbleStripRL', 'OnRumbleStripRR',
    'InPuddleFL', 'InPuddleFR',
    'InPuddleRL', 'InPuddleRR',
    'SurfaceRumbleFL', 'SurfaceRumbleFR',
    'SurfaceRumbleRL', 'SurfaceRumbleRR',
    'SlipAngleFL', 'SlipAngleFR', # 0 = max grip, 1 = min grip
    'SlipAngleRL', 'SlipAngleRR', # lateral
    'SlipCombinedFL', 'SlipCombinedFR', # 0 = max grip, 1 = min grip
    'SlipCombinedRL', 'SlipCombinedRR', # long+lat?
    'SuspAbsFL', 'SuspAbsFR', # compression?
    'SuspAbsRL', 'SuspAbsRR', # in meters
    'CarOrdinal', # unique make/modlel id
    'CarClass',   # enum
    'CarPI',      # performance index
    'Drivetrain', # enum
    'Cylinders', # 0-255
    'CarType', # enum
    'Placeholder2', 'Placeholder3', # unknown
    'PosX', 'PosY', 'PosZ', # position
    'Speed',  # m/s
    'Power',  # W
    'Torque', # Nm
    'TireTempFL', 'TireTempFR',
    'TireTempRL', 'TireTempRR',
    'Boost', # PSI?
    'Fuel',
    'DistTraveled',
    'BestLapTime', 'LastLapTime',
    'CurLapTime', 'CurRaceTime',
    'LapNo', 'RacePos',
    'Throttle', 'Brake', 'Clutch', 'Handbrake', # raw inputs? 0-255
    'Gear', 'Steer', # actual values? 0-255, -127-127
    'DrivingLine', 'AIBrakeDiff' #?
    ]
data_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiiiiIIfffffffffffffffffHBBBBBBbbb'




def unpack(packet):
    return struct.unpack(data_format, packet[0:323])

def read_csv(filepath_or_buffer):
    df = pd.read_csv(filepath_or_buffer)
    if df.shape[1] == 85: # missing "forza placeholders"
        df.insert(58, field_names[58], pd.Series())
        df.insert(59, field_names[59], pd.Series())
        df.insert(60, field_names[60], pd.Series())
    if df.shape[1] != 88:
        return pd.DataFrame() # return empty dataframe if incorrect input file
    df.columns = field_names
    return df
        
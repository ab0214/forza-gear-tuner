# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:28:15 2023

@author: AB0214
"""

import socket
import struct
import time
import binascii
import pandas as pd
import numpy as np
import re
import convert
from collections import namedtuple



data_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiiiiIIfffffffffffffffffHBBBBBBbbb'
field_names = [
    'is_race_on', 'timestamp_ms',
    'engine_max_rpm', 'engine_idle_rpm', 'current_engine_rpm',
    'acceleration_x', 'acceleration_y', 'acceleration_z',
    'velocity_x', 'velocity_y', 'velocity_z',
    'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
    'yaw', 'pitch', 'roll',
    'norm_suspension_travel_FL', 'norm_suspension_travel_FR',
    'norm_suspension_travel_RL', 'norm_suspension_travel_RR',
    'tire_slip_ratio_FL', 'tire_slip_ratio_FR',
    'tire_slip_ratio_RL', 'tire_slip_ratio_RR',
    'wheel_rotation_speed_FL', 'wheel_rotation_speed_FR',
    'wheel_rotation_speed_RL', 'wheel_rotation_speed_RR',
    'wheel_on_rumble_strip_FL', 'wheel_on_rumble_strip_FR',
    'wheel_on_rumble_strip_RL', 'wheel_on_rumble_strip_RR',
    'wheel_in_puddle_FL', 'wheel_in_puddle_FR',
    'wheel_in_puddle_RL', 'wheel_in_puddle_RR',
    'surface_rumble_FL', 'surface_rumble_FR',
    'surface_rumble_RL', 'surface_rumble_RR',
    'tire_slip_angle_FL', 'tire_slip_angle_FR',
    'tire_slip_angle_RL', 'tire_slip_angle_RR',
    'tire_combined_slip_FL', 'tire_combined_slip_FR',
    'tire_combined_slip_RL', 'tire_combined_slip_RR',
    'suspension_travel_meters_FL', 'suspension_travel_meters_FR',
    'suspension_travel_meters_RL', 'suspension_travel_meters_RR',
    'car_ordinal', 'car_class', 'car_performance_index',
    'drivetrain_type', 'num_cylinders',
    'horizon_placeholder1', 'horizon_placeholder2', 'horizon_placeholder3',
    'position_x', 'position_y', 'position_z',
    'speed', 'power', 'torque',
    'tire_temp_FL', 'tire_temp_FR',
    'tire_temp_RL', 'tire_temp_RR',
    'boost', 'fuel', 'dist_traveled',
    'best_lap_time', 'last_lap_time',
    'cur_lap_time', 'cur_race_time',
    'lap_no', 'race_pos',
    'accel', 'brake', 'clutch', 'handbrake',
    'gear', 'steer',
    'norm_driving_line', 'norm_ai_brake_diff'
    ]
test_data = binascii.unhexlify('010000002f3f3428fb6f1446a1639644e17a964470795bba7e57873c338e80bc7d9c6a395a1262baf528773aab5bea3aae08bbb78fee07bad768b53f2b013ebdbf1193bc7f8ec23e9cd5c23eeb27a93e8147ac3e447b1b3e31131a3dca980bbd47c016be00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f20df6bca3fd2abdf074d53ba002343d927e1e3ecd2a663db91f0e3d2c531d3e00013e3a009a4b3a808786ba00a2f6b96a0800000400000084030000010000000a000000130000000000000000000000a93c91c21949cb439fde9145e506aa3a8a5244c08f55c7bc7072584362585b43e6eb7343e6eb7343646630c10000803f0000000000000000000000000000000022004d41000000000000000200000000')




def parse(packet):
    unpacked_data = struct.unpack(data_format, packet[0:323])
    named_data = namedtuple('FH5_telemetry_data', field_names)(*unpacked_data)
    return named_data


def parse_to_df(packet):
    unpacked_data = struct.unpack(data_format, packet[0:323])
    df = pd.DataFrame(unpacked_data, index=field_names)
    #df = df.T
    return df


def parse_to_np(packet):
    unpacked_data = struct.unpack(data_format, packet[0:323])
    
    # Extract format specifiers using regular expressions
    format_specifiers = re.findall(r'([a-zA-Z])', data_format)
    
    # Pair field names with format specifiers
    field_formats = list(zip(field_names, format_specifiers))

    # Create the dtype for the structured array
    dtype = np.dtype(field_formats)
    
    numpy_array = np.rec.array(unpacked_data, dtype=dtype)
    
    return numpy_array


def listen():
    # Set up the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 5300))  # Bind to the IP and port you want to listen on
    
    while True:
        data, addr = sock.recvfrom(1024)  # Receive data from the UDP socket
        telemetry = parse(data)
        
        final_drive = 4.0
        output_rads_per_s = (telemetry.wheel_rotation_speed_RL + 
                             telemetry.wheel_rotation_speed_RR) / 2
        output_rpm = convert.rads_to_rpm(output_rads_per_s)
        if output_rpm != 0 and final_drive != 0:
            ratio = telemetry.current_engine_rpm / output_rpm / final_drive
            print(ratio)
        else:
            print("No data")
    
    sock.close()



numpy_array = parse_to_np(test_data)
fields = ['engine_max_rpm', 'gear']
for field_name in fields:
    value = numpy_array[field_name]
    print(f"{field_name}: {value}")
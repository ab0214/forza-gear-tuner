# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 18:18:35 2023

@author: AB0214
"""

csv_path = 'data/testdata3.csv'
final_drive = 3.85


# Import test data from csv file
import telemetry
telemetry = telemetry.read_csv(csv_path)
print('Data from ' + str(telemetry.shape[0]) + ' telemetry frames.')

# Parse power curve from telemetry data
from power_curve import PowerCurve
power_curve = PowerCurve(telemetry).data

# Detect and print gear ratios
import ratio_detection
gear_ratios = ratio_detection.detect_ratios(telemetry)
for ratio in gear_ratios:
    print(f"{(ratio/final_drive):.2f}")

# Helper function for converting input (at engine) rpm and torque
# to output (at the wheels) rpm and torque
def apply_ratio(engine, gear, ratio):
    output = [
        engine['RPM'],
        engine['Torque'],
        engine['Power'],
        gear,
        engine['RPM'] / ratio,
        engine['Torque'] * ratio]
    return output

# Convert engine power curve to output power curve
outputs = []
for gear, ratio in gear_ratios.items():
    for index, engine in power_curve.iterrows():
        outputs += [apply_ratio(engine, gear, ratio)]

import pandas as pd
outputs = pd.DataFrame(
    outputs, 
    columns=['RPM', 'Torque', 'Power', 'Gear', 'WheelRpm', 'WheelTorque'])
outputs.sort_values(by=['Gear', 'WheelRpm'], inplace=True)

# Detect wheel diameter from telemetry data
d = ratio_detection.detect_wheel_circumference(telemetry)
# Calculate value for converting wheel rpm to speed (km/h)
rpm_to_kmh = d * 60 / 1000


# Draw plot

import seaborn as sns
sns.set_style("white")
plot = sns.lineplot(
    data = outputs,
    x = 'WheelRpm',
    y = 'Power',
    hue = 'Gear'
    )

from matplotlib import ticker
plot.xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda rpm, pos: round(rpm * rpm_to_kmh)))
plot.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda w, pos: round(w/1000)))
plot.set(xlabel='Speed (km/h)', ylabel='Power (kW)')
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 00:27:05 2023

@author: AB0214
"""

import math

# Revolutions per minute to radian per second
def rpm_to_rads(rpm):
    return rpm * math.tau / 60

# Radian per second to revolutions per minute
def rads_to_rpm(rads):
    return rads * 60 / math.tau
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 12:40:47 2023

@author: AB0214
"""

from enum import IntEnum

class CarType(IntEnum):
	MODERN_SUPER_CARS = 11
	RETRO_SUPER_CARS = 12
	HYPER_CARS = 13
	RETRO_SALOONS = 14
	VANS_AND_UTILITY = 16
	RETRO_SPORTS_CARS = 17
	MODERN_SPORTS_CARS = 18
	SUPER_SALOONS = 19
	CLASSIC_RACERS = 20
	CULT_CARS = 21
	RARE_CLASSICS = 22
	SUPER_HOT_HATCH = 25
	RODS_AND_CUSTOMS = 29
	RETRO_MUSCLE = 30
	MODERN_MUSCLE = 31
	RETRO_RALLY = 32
	CLASSIC_RALLY = 33
	RALLY_MONSTERS = 34
	MODERN_RALLY = 35
	GT_CARS = 36
	SUPER_GT = 37
	EXTREME_OFFROAD = 38
	SPORTS_UTILITY_HEROES = 39
	OFFROAD = 40
	OFFROAD_BUGGIES = 41
	CLASSIC_SPORTS_CARS = 42
	TRACK_TOYS = 43
	VINTAGE_RACERS = 44
	TRUCKS = 45
    
class CarClass(IntEnum):
    D = 0
    C = 1
    B = 2
    A = 3
    S1 = 4
    S2 = 5
    X = 6
    
class DriveTrainType(IntEnum):
    FWD = 0
    RWD = 1
    AWD = 2
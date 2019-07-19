# import necessary packages

import glob
import os
import sys
import time

sys.path.append('/home/nashita/UnrealEngine_4.22/carla/Dist/CARLA_0.9.5-428-g0ce908d-dirty/LinuxNoEditor/PythonAPI/carla/dist/carla-0.9.5-py3.5-linux-x86_64.egg')

import carla
import argparse
import logging
import random
import math
import numpy as np
import decimal
from PedestrianCrossRoad import spawn 

# to connect to a simulator we need to create a "Client" object 
# provide the IP address and port of a running instance of the simulator

_HOST_ = '127.0.0.1'
_PORT_ = 2000

client = carla.Client(_HOST_, _PORT_)

# to connect to a simulator we need to create a "Client" object, to do so 
# provide the IP address and port of a running instance of the simulator

_SLEEP_TIME_ = 1

# once the client is configured, directly retrieve the world

world = client.get_world()

# get a list of all pedestrians from the blueprint library and choose one randomly

blueprintsWalkers = world.get_blueprint_library().filter("walker.pedestrian.0013")
random_walker_bp = random.choice(blueprintsWalkers)

# variables in order to directly retrieve certain methods/classes 

librarycarla = carla.libcarla
world = client.get_world()
maps = world.get_map()
tran = librarycarla.Transform
loc = librarycarla.Location
rot = librarycarla.Rotation

# define spawn point

recommended_spawn_points = world.get_map().get_spawn_points() # spawn points from carla
spawn_sidewalk_corner = recommended_spawn_points[1] # used to set rotation class before location is changed
spawn_sidewalk_corner.location = loc(x = 180.12558, y=76.188217, z=1)
# cross street loc: loc(x=175.29485, y=75.488579, z=0.91) 
# default: loc(x=190.3622, y=71.4094, z=1)

# define spawn destination

spawn_destination = recommended_spawn_points[0] # used to set rotation class before location is changed
spawn_destination.location = loc(x=158.13466, y=75.964157, z=0.91)

# set weather in simulation to sunny so the pedestrian is easier to see

weather = carla.WeatherParameters(cloudyness=0.0,precipitation=0.0,sun_altitude_angle=90.0)
world.set_weather(weather)

# test PedestrianCrossRoad script

list_of_averages = []

def tester(bp, transform1, transform2, speed, count):
	list_of_differences = []
	for i in range(count):
		list_of_differences.append( spawn(bp, transform1, transform2, speed) )

	total = 0
	for diff in list_of_differences:
		total += diff

	average = total/count
	list_of_averages.append (average)

tester(random_walker_bp, spawn_sidewalk_corner, spawn_destination, 20, 100)
print (list_of_averages)
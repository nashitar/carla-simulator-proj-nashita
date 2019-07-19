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
spawn_sidewalk_corner.location = loc(x = 170.12558, y=76.188217, z=1)
# cross street loc: loc(x=175.29485, y=75.488579, z=0.91) 
# default: loc(x=190.3622, y=71.4094, z=1)

# define spawn destination

spawn_destination = recommended_spawn_points[0] # used to set rotation class before location is changed
spawn_destination.location = loc(x=158.13466, y=75.964157, z=0.91)

# set weather in simulation to sunny so the pedestrian is easier to see

weather = carla.WeatherParameters(cloudyness=0.0,precipitation=0.0,sun_altitude_angle=90.0)
world.set_weather(weather)

# spawn pedestrian at a certain angle for a specified amount of time

def spawn (bp, transform1, transform2, speed):

	# define a pedestrian to spawn at the initial location

	pedestrian = world.spawn_actor(bp, transform1)
	
	# calculate the distance the pedestrian needs to travel in the x and y direction
	# the z direction is immaterial at this point

	x = transform2.location.x - transform1.location.x
	y = transform2.location.y - transform1.location.y

	# values assigned to control.direction.* need to be between -1 and 1

	if (abs(x) >= abs(y)):
		if (abs(x) >= 0 and abs(x) < 1):
			x_for_det_angle = x/1
			y_for_det_angle = y/1
		elif (abs(x) >= 1 and abs(x) < 10):
			x_for_det_angle = x/10
			y_for_det_angle = y/10
		elif (abs(x) >= 10 and abs(x) < 100):
			x_for_det_angle = x/100
			y_for_det_angle = y/100
		elif (abs(x) >= 10 and abs(x) < 100):
			x_for_det_angle = x/1000
			y_for_det_angle = y/1000
		else:
			print (":(")
	else:
		if (abs(y) >= 0 and abs(y) < 1):
			y_for_det_angle = y/1
			x_for_det_angle = x/1
		elif (abs(y) >= 1 and abs(y) < 10):
			y_for_det_angle = y/10
			x_for_det_angle = x/10
		elif (abs(y) >= 10 and abs(y) < 100):
			y_for_det_angle = y/100
			x_for_det_angle = x/100
		elif (abs(y) >= 10 and abs(y) < 100):
			y_for_det_angle = y/1000
			x_for_det_angle = x/1000
		else:
			print (":(")	

	# calculate distance being traveled by pedestrian and time
	
	hyp = math.sqrt( math.pow(x,2) + math.pow(y,2) )
	seconds = hyp / speed

	# create buffer for time it takes to "climb" sidewalk

	# carla has actors of three different general sizes: 
	# 	adults, who have the shortest buffer periods, 
	#	teenagers, who have medium length buffer periods
	# 	and kids, who have long buffer periods
	#
	# assuming carla releases more pedestrian blueprints, which is more than likely, 
	# it is unfeasible to organize added seconds by blueprint "name", especially
	# when taking into consideration that blueprint names, after specifying the 
	# type of blueprint (pedestrians), are nothing more than numbers. as such, the 
	# added buffer time was calculated by finding the necessary buffer time for each
	# blueprint that exists in the built from scratch 0.9.x version of CARLA
	#

	seconds += 0
	
	# tell the pedestrian to move for the requested number of seconds

	while seconds >= 0: 
		control = carla.WalkerControl()
		control.speed = speed # speed is defined in m/s
		control.direction.y = y_for_det_angle
		control.direction.x = x_for_det_angle
		pedestrian.apply_control(control)
		time.sleep(1.0)

		seconds -= 0.2

	# stop the pedestrian

	control.speed = 0
	pedestrian.apply_control(control)
	
	final_location = pedestrian.get_location()
	x_difference  = spawn_destination.location.x - final_location.x
	y_difference  = spawn_destination.location.y - final_location.y
	exact_difference = math.sqrt( math.pow(x_difference,2) + math.pow(y_difference,2) )

	pedestrian.destroy()

	return exact_difference

spawn(random_walker_bp, spawn_sidewalk_corner, spawn_destination, 7)

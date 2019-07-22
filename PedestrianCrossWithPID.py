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
from numpy import linalg as la
import decimal 

sys.path.append('/home/nashita/Downloads/simple_pid/simple_pid/PID.py')
from simple_pid import PID

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

blueprintsWalkers = world.get_blueprint_library().filter("walker.pedestrian.*")
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
spawn_sidewalk_corner.location = loc(x = 170.12558, y=76.188217, z=1.1)

# define spawn destination

set_point = recommended_spawn_points[0] # used to set rotation class before location is changed
set_point.location = loc(x=163.13466, y=65.964157, z=0.91)

# set weather in simulation to sunny so the pedestrian is easier to see

weather = carla.WeatherParameters(cloudyness=0.0,precipitation=0.0,sun_altitude_angle=90.0)
world.set_weather(weather)

# define a pedestrian to spawn at the initial location

pedestrian = world.spawn_actor(random_walker_bp, spawn_sidewalk_corner)

# spawn pedestrian at a certain angle for a specified amount of time

def spawn (pedestrian, initial, sp, seconds=5, speed=1):

	# set initial values for pid controller and create variable that will 
	# track the location of the pedestrian throughout its path

	pid = PID(3, 0.01, 0.1, setpoint=sp)
	current = initial.location

	# make sure method to find inital angle does not result in out of bounds 
	# error and find initial angle

	if (((initial.location.y/initial.location.x) > 1) or ((initial.location.y/initial.location.x) < -1)):
		initial_angle = math.acos(initial.location.x/initial.location.y)
	else:
		initial_angle = math.asin(initial.location.y/initial.location.x)	

	# tell the pedestrian to move for the requested number of seconds 
	# or until the destination is reached

	while seconds >= 0: 

		# create control variable in order to track and control 
		# pedestrain movement and set basic values

		control = carla.WalkerControl()
		control.speed = speed # speed is defined in m/s

		# set value of pedestrain location in order to avoid null error

		null_loc = loc(x=0, y=0, z=0)

		if (pedestrian.get_location() != null_loc):
			current = pedestrian.get_location()
		else:
			current = initial.location

		# values assigned to control.direction.* need to be between -1 and 1

		x = sp.location.x - current.x 
		y = sp.location.y - current.y

		if (abs(x) >= abs(y)):
			if (abs(x) >= 1 and abs(x) < 10):
				x = x/10
				y = y/10
			elif (abs(x) >= 10 and abs(x) < 100):
				x = x/100
				y = y/100
			elif (abs(x) >= 10 and abs(x) < 100):
				x = x/1000
				y = y/1000
		else:
			if (abs(y) >= 1 and abs(y) < 10):
				y = y/10
				x = x/10
			elif (abs(y) >= 10 and abs(y) < 100):
				y = y/100
				x = x/100
			elif (abs(y) >= 10 and abs(y) < 100):
				y = y/1000
				x = x/1000

		# set pedestrian direction

		control.direction.y = y
		control.direction.x = x

		# apply the values set to the control variable to the pedestrian

		pedestrian.apply_control(control)
		time.sleep(1.0)

		# make sure method to find set point angle does not result in  
		# out of bounds error and find set point angle

		if (((control.direction.y/control.direction.x) > 1) or ((control.direction.y/control.direction.x) < -1)):
			sp_angle = math.acos(control.direction.x/control.direction.y)
		else:
			sp_angle = math.asin(control.direction.y/control.direction.x)

		# calculate angle error

		angle_error = initial_angle - sp_angle

		# find norm

		sp_as_vector = [sp.location.x, sp.location.y, sp.location.z]
		p_as_vector = [current.x, current.y, current.z]
		
		calculate_norm = []

		for i in range(3):
			calculate_norm.append( sp_as_vector[i] - p_as_vector[i] )
		
		L_error = la.norm( calculate_norm )

		# use PID to update value of angle and L

		angle_update = PID(angle_error)
		L_update = PID(L_error)

		# update the seconds

		seconds -= 0.2

		# if location is reached, stop running the loop

		if (abs(sp.location.x - pedestrian.get_location().x) <= 0.3):
			if (abs(sp.location.y - pedestrian.get_location().y) <= 0.3):
				seconds = -1

	# stop the pedestrian

	control.speed = 0
	pedestrian.apply_control(control)

# run the method

spawn (pedestrian, spawn_sidewalk_corner, set_point)

set_point_2 = recommended_spawn_points[0] # used to set rotation class before location is changed
set_point_2.location = loc(x=173.13466, y=85.964157, z=0.91)

spawn (pedestrian, set_point, set_point_2)

# destroy the pedestrian once complete

pedestrian.destroy()

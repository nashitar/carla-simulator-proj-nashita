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
# cross street loc: loc(x=175.29485, y=75.488579, z=0.91) 
# default: loc(x=190.3622, y=71.4094, z=1)

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

	pid = PID(3, 0.01, 0.1, setpoint=sp)

	current = initial.location

	# values assigned to control.direction.* need to be between -1 and 1

	x = sp.location.x - current.x 
	y = sp.location.y - current.y

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

	if (((initial.location.y/initial.location.x) > 1) or ((initial.location.y/initial.location.x) < -1)):
		initial_angle = math.acos(initial.location.x/initial.location.y)
	else:
		initial_angle = math.asin(initial.location.y/initial.location.x)	

	# tell the pedestrian to move for the requested number of seconds

	while seconds >= 0: 
		control = carla.WalkerControl()

		control.speed = speed # speed is defined in m/s

		current = pedestrian.get_location()

		# values assigned to control.direction.* need to be between -1 and 1

		x = sp.location.x - current.x 
		y = sp.location.y - current.y

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

		control.direction.y = y_for_det_angle
		control.direction.x = x_for_det_angle

		pedestrian.apply_control(control)
		time.sleep(1.0)

		if (((control.direction.y/control.direction.x) > 1) or ((control.direction.y/control.direction.x) < -1)):
			sp_angle = math.acos(control.direction.x/control.direction.y)
		else:
			sp_angle = math.asin(control.direction.y/control.direction.x)

		angle_error = initial_angle - sp_angle

		sp_as_vector = [sp.location.x, sp.location.y, sp.location.z]
		p_as_vector = [current.x, current.y, current.z]
		
		calculate_norm = []

		for i in range(3):
			calculate_norm.append( sp_as_vector[i] - p_as_vector[i] )
		
		L_error = la.norm( calculate_norm )

		angle_update = PID(angle_error)
		L_update = PID(L_error)
		#speed = L_update

		seconds -= 0.2

		if (abs(sp.location.x - pedestrian.get_location().x) <= 0.3):
			if (abs(sp.location.y - pedestrian.get_location().y) <= 0.3):
				seconds = -1

	# stop the pedestrian

	control.speed = 0
	pedestrian.apply_control(control)

spawn (pedestrian, spawn_sidewalk_corner, set_point, 4, 5)

pedestrian.destroy()
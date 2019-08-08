# import necessary packages

import glob
import os
import sys
import time

sys.path.append('/home/nashita/UnrealEngine_4.22/carla/Dist/CARLA_0.9.5-428-g0ce908d-dirty/LinuxNoEditor/PythonAPI/carla/dist/carla-0.9.5-py3.5-linux-x86_64.egg')

import carla
import signal
import random
import math
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plot
from Pedestrian import Pedestrian
from CrosswalkPedestrian import CrosswalkPedestrian

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

# get a list of all pedestrians from the blueprint library

blueprintsWalkers = world.get_blueprint_library().filter("walker.pedestrian.*")

# variables in order to directly retrieve certain methods/classes 

librarycarla = carla.libcarla
world = client.get_world()
loc = librarycarla.Location

# set weather in simulation to sunny so the pedestrian is easier to see

weather = carla.WeatherParameters(cloudyness=0.0,precipitation=0.0,sun_altitude_angle=90.0)
world.set_weather(weather)


class LawfulCrosswalkPedestrian(CrosswalkPedestrian):

	# ***** parameters *****
	# 1. pedestrian walks within the bounds of the crosswalk
	# 2. pedestrian walks when car is stopped at stop sign
	# 3. pedestrian walks when traffic light is red (walk sign is white)
	# 4. randomized path movement

	def __init__(self, location):

		super(LawfulCrosswalkPedestrian, self).__init__(location)

	def path (x1, x2, x3, x4, y1, y2, y3, y4):

		# ***********************
		# pedestrian must stay 
		# within the constraints 
		# ***********************
		
		coordinates = []

		spawn_coordinates = CrosswalkPedestrian.spawn()
		for coordinate in spawn_coordinates:
			coordinates.append(coordinate)

		# add a location to the list of coordinates that
		# is on the sidewalk but not near the transition 
		# area between the sdewalk and the crosswalk
		
		coordinates.append(CrosswalkPedestrian.walking_on_sidewalk(x1, x2, y1, y2))

		# create two lists that store the x and y bounds of the crosswalk

		x = [x1, x2, x3, x4]
		y = [y1, y2, y3, y4]

		# check which direction the crosswalk is positioned towards (x or y)

		if ((max(x)-min(x))>(max(y)-min(y))):

			# check whether the first inputted bound is larger or not

			if (x2 > x1):

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the crosswalk

				coordinates.append(CrosswalkPedestrian.transition_point(x1-1, x1, y1, y2))
			else:
				coordinates.append(CrosswalkPedestrian.transition_point(x2-1, x2, y1, y2))
		
		else:

			# check whether the first inputted bound is larger or not

			if (y2 > y1):

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the crosswalk
				
				coordinates.append(CrosswalkPedestrian.transition_point(x1, x2, y1-1, y1))
			else:
				coordinates.append(CrosswalkPedestrian.transition_point(x1, x2, y2-1, y2))

		# add a random number of points to the coordinates list that are along the crosswalk

		path_list = CrosswalkPedestrian.on_path(x1, x2, y1, y2)

		for locations in path_list:
			coordinates.append(locations)

		# check which direction the crosswalk is positioned towards (x or y)

		if ((max(x)-min(x))>(max(y)-min(y))):

			# check whether the first inputted bound is larger or not

			if (x4 > x3):

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the crosswalk

				coordinates.append(CrosswalkPedestrian.transition_point(x4-1, x4, y3, y4))
			else:
				coordinates.append(CrosswalkPedestrian.transition_point(x3-1, x3, y3, y4))
		
		else:
			
			# check whether the first inputted bound is larger or not

			if (y4 > y3):

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the crosswalk

				coordinates.append(CrosswalkPedestrian.transition_point(x3, x4, y4-1, y4))
			else:
				coordinates.append(CrosswalkPedestrian.transition_point(x3, x4, y3-1, y3))

		# add a location to the list of coordinates that
		# is on the sidewalk but not near the transition 
		# area between the sdewalk and the crosswalk
		
		coordinates.append(CrosswalkPedestrian.walking_on_sidewalk(x3, x4, y3, y4))

		coordinates.append(loc(x=158.300598, y=73.316467, z=1.0)) # example final destination point
		#coordinates.append(loc(x=158.973343, y=85.52278, z=1.0)) # example final destination point
		
		# return the list of coordinates

		return coordinates

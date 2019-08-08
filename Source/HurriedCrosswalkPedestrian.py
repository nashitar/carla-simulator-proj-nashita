# import necessary packages

import glob
import os
import sys
import time
from ..Configuration import carla_path

sys.path.append(carla_path)

import carla
import signal
import random
import math
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plot
from .CrosswalkPedestrian import CrosswalkPedestrian

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


class HurriedCrosswalkPedestrian(CrosswalkPedestrian):

	# ***** parameters *****
	# 1. pedestrian spends range of time within the bounds of crosswalk
	# 2. pedestrian spends rest of time outside bounds of crosswalk
	# 3. pedestrian may start when walk sign is red (traffic light is green or 
	#    yellow) but finishes journey when walk sign is white (or vise-versa)
	# 4. randomized path movement
	
	def __init__(self, location):

		super(HurriedCrosswalkPedestrian, self).__init__(location)

	coordinates = []

	def path (x1, x2, x3, x4, y1, y2, y3, y4):

		# ***********************
		# pedestrian must stay 
		# within and exit the
		# bounds of the constraints 
		# ***********************

		coordinates = []

		spawn_coordinates = CrosswalkPedestrian.spawn()
		for coordinate in spawn_coordinates:
			coordinates.append(coordinate)

		# choose whethet the pedestrian is going to start on the left or the right

		left_or_right = random.choice([1, 2])

		# create two lists that store the x and y bounds of the crosswalk

		x = [x1, x2, x3, x4]
		y = [y1, y2, y3, y4]

		# check which direction the crosswalk is positioned towards (x or y)

		if ((max(x)-min(x))>(max(y)-min(y))):

			# if the variable left_or_right is equal to 1 the padestrian is going left

			if (left_or_right == 1):

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				coordinates.append(CrosswalkPedestrian.transition_point(x1, x2, y1-3, y1-1))
				
				# add a random number of points to the coordinates list that are along the crosswalk

				path_list = CrosswalkPedestrian.on_path(x1, x2, y1-3, y1-1)
				for locations in path_list:
					coordinates.append(locations)

				# check whether the first inputted bound is larger or not
				# and add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				if (x4 > x3):
					coordinates.append(CrosswalkPedestrian.transition_point(x4-1, x4, y3, y4))
				else:
					coordinates.append(CrosswalkPedestrian.transition_point(x3-1, x3, y3, y4))
		
			# if the variable left_or_right is equal to 2 the padestrian is going right
			
			else:

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				coordinates.append(CrosswalkPedestrian.transition_point(x1, x2, y2+1, y2+3))

				# add a random number of points to the coordinates list that are along the crosswalk

				path_list = CrosswalkPedestrian.on_path(x1, x2, y2+1, y2+3)
				for locations in path_list:
					coordinates.append(locations)

				# check whether the first inputted bound is larger or not
				# and add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				if (x4 > x3):
					coordinates.append(CrosswalkPedestrian.transition_point(x4-1, x4, y3, y4))
				else:
					coordinates.append(CrosswalkPedestrian.transition_point(x3-1, x3, y3, y4))

		# else of conditional used to check which direction the crosswalk is positioned towards

		else:

			# if the variable left_or_right is equal to 1 the padestrian is going left

			if (left_or_right == 1):

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				coordinates.append(CrosswalkPedestrian.transition_point(x1-3, x1-1, y1, y2))

				# add a random number of points to the coordinates list that are along the crosswalk

				path_list = CrosswalkPedestrian.on_path(x1-3, x1-1, y1, y2)
				for locations in path_list:
					coordinates.append(locations)

				# check whether the first inputted bound is larger or not
				# and add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				if (y4 > y3):
					coordinates.append(CrosswalkPedestrian.transition_point(x3, x4, y4-1, y4))
				else:
					coordinates.append(CrosswalkPedestrian.transition_point(x3, x4, y3-1, y3))

			else:

				# add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				coordinates.append(CrosswalkPedestrian.transition_point(x2+1, x2+3, y1, y2))

				# add a random number of points to the coordinates list that are along the crosswalk

				path_list = CrosswalkPedestrian.on_path(x2+1, x2+3, y1, y2)
				for locations in path_list:
					coordinates.append(locations)

				# check whether the first inputted bound is larger or not
				# and add a point to coordinates that acts as a transition 
				# point between the sidewalk and the road

				if (y4 > y3):
					coordinates.append(CrosswalkPedestrian.transition_point(x3, x4, y4-1, y4))
				else:
					coordinates.append(CrosswalkPedestrian.transition_point(x3, x4, y3-1, y3))

		coordinates.append(loc(x=158.300598, y=73.316467, z=1.0)) # example final destination point
		#coordinates.append(loc(x=157.973343, y=100.52278, z=1.0)) # example final destination point

		# return the list of coordinates

		return coordinates

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
import scipy.stats as stats

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

class CrosswalkPedestrian(Pedestrian):
	
	def __init__(self, location):

		super(CrosswalkPedestrian, self).__init__(location)

	# ***** crosswalk 1 *****
	
	# select spawn point along crosswalk

	def spawn ():

		coordinates = []
		spawn_locations = [
			loc(x=179.1955, y=95.1132, z=1.0),
			loc(x=179.3619, y=99.5992, z=1.0),
			loc(x=175.1989, y=111.8594, z=1.0),
			loc(x=160.5533, y=131.2093, z=2.0), 
			loc(x=154.0178, y=134.9659, z=3.0),
			loc(x=138.7439, y=140.6069, z=2.0),
			loc(x=117.2375, y=141.6584, z=2.0),
			loc(x=106.9878, y=142.0408, z=1.0),  
			loc(x=95.8213, y=142.4594, z=1.0), 
			loc(x=67.9693, y=142.6978, z=1.0)]

		distance = random.randint(0,10)

		# if the selected spawn point is far from the 
		# crosswalk, more points along the sidewalk have 
		# to be added to the list so that the pedestrian 
		# doesn't get stuck anywhere
		
		for i in range (distance):
			coordinates.append(spawn_locations[distance-i-1])
		
		return coordinates

	# method to return the transition point pf the
	# pedestrian by randomly selecting a point along 
	# a gaussian distribution

	def transition_point (x1, x2, y1, y2):
		
		# set position

		recommended_points = world.get_map().get_spawn_points() # spawn points from carla
		point = recommended_points[1] # used to set rotation class before location is changed

		# choose randomized position

		# pick random coordinates

		lower_x, upper_x = x1, x2 # lower and upper bounds for x values
		mu_x = (x1+x2)/2 # mean for the x values
		sigma_x = (abs(x2-x1-0.5))/2 # standard deviation for the x

		# use a truncated normal distribution to select points so that 
		# they still radiate out from a central mean but are bounded

		x = stats.truncnorm(((lower_x - mu_x) / sigma_x), ((upper_x - mu_x) / sigma_x), loc=mu_x, scale=sigma_x)
		x_coordinate = x.rvs(100000)

		lower_y, upper_y = y1, y2 # lower and upper bounds for y values
		mu_y = (y1+y2)/2 # mean for the y values
		sigma_y = (abs(y2-y1-0.5))/2 # standard deviation for the y

		# use a truncated normal distribution to select points so that 
		# they still radiate out from a central mean but are bounded

		y = stats.truncnorm((lower_y - mu_y) / sigma_y, (upper_y - mu_y) / sigma_y, loc=mu_y, scale=sigma_y)
		y_coordinate = y.rvs(100000)

		# set initial z value to 1 for any random x-y pair

		z_coordinate = [1.0 for _ in range(100000)]

		# create list of locations using random coordinates
		
		list_of_coordinates = list(map(lambda coord: loc(x=coord[0],y=coord[1],z=coord[2]), zip(x_coordinate,y_coordinate,z_coordinate)))

		# select a random point from the generated list

		point.location = random.choice(list_of_coordinates)
		return point.location

	# method to return the spawn point and the
	# destination point of the pedestrian by randomly
	# selecting a point along a uniform distribution

	def walking_on_sidewalk (x1, x2, y1, y2):

		# set position

		recommended_points = world.get_map().get_spawn_points() # spawn points from carla
		point = recommended_points[1] # used to set rotation class before location is changed

		# create lists

		x_coordinate = []
		y_coordinate = []
		z_coordinate = []

		# choose randomized position

		# pick random coordinates (uniformly select between the given x and y bounds)

		for i in range(100000):
			x_coordinate.append(random.uniform(x1,x2))
			y_coordinate.append(random.uniform(y1,y2))
			z_coordinate.append(1.0) # set initial z value to 1 for any random x-y pair

		# create list of locations using random coordinates
		
		list_of_coordinates = list(map(lambda coord: loc(x=coord[0],y=coord[1],z=coord[2]), zip(x_coordinate,y_coordinate,z_coordinate)))

		point.location = random.choice(list_of_coordinates)
		return point.location

	# method to select between one and three
	# locations along the path with some measure
	# of randomness

	def on_path (x1, x2, y1, y2):

		# either have two, three, or four random points on 
		# the crosswalk for the pedestrian to walk through 

		number_of_points = random.choice([2, 3, 4])

		# the use of normal or uniform distribution for choosing
		# coordinates is reliant on whether the the length of the
		# crosswalk is the x or the y

		def pick_coordinates (x1, x2, y1, y2):
			
			# create two lists to store the bounds of the x and y coordinates
			
			x = [x1, x2]
			y = [y1, y2]

			if ((max(x)-min(x))>(max(y)-min(y))):

				# the y constraints are the ones that the pedestrian 
				# should use normal distribution to randomly select 
				# from and the x constraints are the ones that the pedestrian
				# should use uniform distribution to select from

				# create lists to store x and y coordinates

				x_coordinate = []
				y_coordinate = []
				
				for i in range(100000):
					x_coordinate.append(random.uniform(x1,x2))

				lower_y, upper_y = y1, y2 # lower and upper bounds for y values
				mu_y = (y1+y2)/2 # mean for the y values
				sigma_y = (abs(y2-y1-2))/2 # standard deviation for the y

				# use a truncated normal distribution to select points so that 
				# they still radiate out from a central mean but are bounded

				y = stats.truncnorm((lower_y - mu_y) / sigma_y, (upper_y - mu_y) / sigma_y, loc=mu_y, scale=sigma_y)
				y_coordinate = y.rvs(100000)

				# set initial z value to 1 for any random x-y pair
				
				z_coordinate = [1.0 for _ in range(100000)]

				# return list of locations using random coordinates
		
				return list(map(lambda coord: loc(x=coord[0],y=coord[1],z=coord[2]), zip(x_coordinate,y_coordinate,z_coordinate)))

			else: 

				# the x constraints are the ones that the pedestrian 
				# should use normal distribution to randomly select 
				# from and the y constraints are the ones that the pedestrian
				# should use uniform distribution to select from

				# create lists to store x and y coordinates

				y_coordinate = []
				x_coordinate = []
				
				for i in range(100000):
					y_coordinate.append(random.uniform(y1,y2))

				lower_x, upper_x = x1, x2 # lower and upper bounds for x values
				mu_x = (x1+x2)/2 # mean for the x values
				sigma_x = (abs(x2-x1-2))/2 # standard deviation for the x

				# use a truncated normal distribution to select points so that 
				# they still radiate out from a central mean but are bounded

				x = stats.truncnorm((lower_x - mu_x) / sigma_x, (upper_x - mu_x) / sigma_x, loc=mu_x, scale=sigma_x)
				x_coordinate = x.rvs(100000)

				# set initial z value to 1 for any random x-y pair
				
				z_coordinate = [1.0 for _ in range(100000)]

				# return list of locations using random coordinates
		
				return list(map(lambda coord: loc(x=coord[0],y=coord[1],z=coord[2]), zip(x_coordinate,y_coordinate,z_coordinate)))


		if (number_of_points == 2):

			# set position

			recommended_points = world.get_map().get_spawn_points() # spawn points from carla
			point_1 = recommended_points[1] # used to set rotation class before location is changed
			point_2 = recommended_points[1] # used to set rotation class before location is changed

			# pick random coordinates

			# create lists to store x and y bounds

			x = [x1, x2]
			y = [y1, y2]

			# check which direction the crosswalk is positioned towards (x or y)

			if ((max(x)-min(x))>(max(y)-min(y))):

				# pick a coordinate in the first half of the crosswalk

				list_of_coordinates_1 = pick_coordinates (x1, (x2 - (0.5*(x2-x1))), y1, y2)
				point_1.location = random.choice(list_of_coordinates_1)

				# pick a coordinate in the second half of the crosswalk

				list_of_coordinates_2 = pick_coordinates ((x1 + (0.5*(x2-x1))), x2, y1, y2)
				point_2.location = random.choice(list_of_coordinates_2)
				
				# return the coordinates

				return [point_1.location, point_2.location]

			else:
				
				# pick a coordinate in the first half of the crosswalk

				list_of_coordinates_1 = pick_coordinates (x1, x2, y1, (y2 - (0.5*(y2-y1))))
				point_1.location = random.choice(list_of_coordinates_1)

				# pick a coordinate in the second half of the crosswalk

				list_of_coordinates_2 = pick_coordinates (x1, x2, (y1  + (0.5*(y2-y1))), y2)
				point_2.location = random.choice(list_of_coordinates_2)
				
				# return the coordinates

				return [point_1.location, point_2.location]

		elif (number_of_points == 3):

			# set position

			recommended_points = world.get_map().get_spawn_points() # spawn points from carla
			point_1 = recommended_points[1] # used to set rotation class before location is changed
			point_2 = recommended_points[1] # used to set rotation class before location is changed
			point_3 = recommended_points[1] # used to set rotation class before location is changed

			# pick random coordinates

			# create lists to store x and y bounds

			x = [x1, x2]
			y = [y1, y2]

			# check which direction the crosswalk is positioned towards (x or y)

			if ((max(x)-min(x))>(max(y)-min(y))):

				# pick a coordinate in the first third of the crosswalk

				list_of_coordinates_1 = pick_coordinates (x1, (x2 - ((2/3)*(x2-x1))), y1, y2)
				point_1.location = random.choice(list_of_coordinates_1)

				# pick a coordinate in the second third of the crosswalk

				list_of_coordinates_2 = pick_coordinates ((x1 + ((1/3)*(x2-x1))), (x2 - ((1/3)*(x2-x1))), y1, y2)
				point_2.location = random.choice(list_of_coordinates_2)

				# pick a coordinate in the final third of the crosswalk

				list_of_coordinates_3 = pick_coordinates ((x1 + ((2/3)*(x2-x1))), x2, y1, y2)
				point_3.location = random.choice(list_of_coordinates_3)
				
				# return the coordinates

				return [point_1.location, point_2.location, point_3.location]

			else:

				# pick a coordinate in the first third of the crosswalk

				list_of_coordinates_1 = pick_coordinates (x1, x2, y1, (y2 - ((2/3)*(y2-y1))))
				point_1.location = random.choice(list_of_coordinates_1)

				# pick a coordinate in the second third of the crosswalk

				list_of_coordinates_2 = pick_coordinates (x1, x2, (y1 + ((1/3)*(y2-y1))), (y2 - ((1/3)*(y2-y1))))
				point_2.location = random.choice(list_of_coordinates_2)

				# pick a coordinate in the final third of the crosswalk

				list_of_coordinates_3 = pick_coordinates (x1, x2, (y1 + ((2/3)*(y2-y1))), y2)
				point_3.location = random.choice(list_of_coordinates_3)
				
				# return the coordinates

				return [point_1.location, point_2.location, point_3.location]


		else:

			# set position

			recommended_points = world.get_map().get_spawn_points() # spawn points from carla
			point_1 = recommended_points[1] # used to set rotation class before location is changed
			point_2 = recommended_points[1] # used to set rotation class before location is changed
			point_3 = recommended_points[1] # used to set rotation class before location is changed
			point_4 = recommended_points[1] # used to set rotation class before location is changed

			# pick random coordinates

			# create lists to store x and y bounds

			x = [x1, x2]
			y = [y1, y2]

			# check which direction the crosswalk is positioned towards (x or y)

			if ((max(x)-min(x))>(max(y)-min(y))):

				# pick a coordinate in the first quarter of the crosswalk

				list_of_coordinates_1 = pick_coordinates (x1, (x2 - ((3/4)*(x2-x1))), y1, y2)
				point_1.location = random.choice(list_of_coordinates_1)

				# pick a coordinate in the second quarter of the crosswalk

				list_of_coordinates_2 = pick_coordinates ((x1 + ((1/4)*(x2-x1))), (x2 - ((1/2)*(x2-x1))), y1, y2)
				point_2.location = random.choice(list_of_coordinates_2)

				# pick a coordinate in the third quarter of the crosswalk

				list_of_coordinates_3 = pick_coordinates ((x1 + ((1/2)*(x2-x1))), (x2 - ((1/4)*(x2-x1))), y1, y2)
				point_3.location = random.choice(list_of_coordinates_3)

				# pick a coordinate in the final quarter of the crosswalk

				list_of_coordinates_4 = pick_coordinates ((x1 + ((3/4)*(x2-x1))), x2, y1, y2)
				point_4.location = random.choice(list_of_coordinates_4)
				
				# return the coordinates

				return [point_1.location, point_2.location, point_3.location, point_4.location]

			else:

				# pick a coordinate in the first quarter of the crosswalk

				list_of_coordinates_1 = pick_coordinates (x1, x2, y1, (y2 - ((3/4)*(y2-y1))))
				point_1.location = random.choice(list_of_coordinates_1)

				# pick a coordinate in the second quarter of the crosswalk

				list_of_coordinates_2 = pick_coordinates (x1, x2, (y1 + ((1/4)*(y2-y1))), (y2 - ((1/2)*(y2-y1))))
				point_2.location = random.choice(list_of_coordinates_2)

				# pick a coordinate in the third quarter of the crosswalk

				list_of_coordinates_3 = pick_coordinates (x1, x2, (y1 + ((1/2)*(y2-y1))), (y2 - ((1/4)*(y2-y1))))
				point_3.location = random.choice(list_of_coordinates_3)

				# pick a coordinate in the final quarter of the crosswalk

				list_of_coordinates_4 = pick_coordinates (x1, x2, (y1 + ((3/4)*(y2-y1))), y2)
				point_4.location = random.choice(list_of_coordinates_4)
				
				# return the coordinates

				return [point_1.location, point_2.location, point_3.location, point_4.location]

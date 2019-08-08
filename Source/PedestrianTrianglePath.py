# import necessary packages
 
import glob
import os
import sys
import time
from ..Configuration import carla_path

sys.path.append(carla_path)

import carla
import logging
import random
import math
import numpy as np

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
loc = librarycarla.Location

# define spawn point

recommended_spawn_points = world.get_map().get_spawn_points() # spawn points from carla
initial = recommended_spawn_points[1] # used to set rotation class before location is changed
initial.location = loc(x = 173.12558, y=90.188217, z=1)

# set weather in simulation to sunny so the pedestrian is easier to see

weather = carla.WeatherParameters(cloudyness=0.0,precipitation=0.0,sun_altitude_angle=90.0)
world.set_weather(weather)

# spawn pedestrian at a certain angle for a specified amount of time

def triangle (bp, start, speed=5):

	# define a pedestrian to spawn at the initial location

	pedestrian = world.spawn_actor(bp, start)
	 
	# make first line of triangle 

	line1 = 2

	while line1 > 0: 
		control = carla.WalkerControl()
		control.speed = speed # speed is defined in m/s
		control.direction.x = -1
		control.direction.y = 0
		
		pedestrian.apply_control(control)
		time.sleep(1.0)

		line1 -= 1

	# stop the pedestrian

	control.speed = 0
	pedestrian.apply_control(control)

	# make second line of triangle 

	line2 = 2

	while line2 > 0:
		control = carla.WalkerControl()
		control.speed = speed # speed is defined in m/s
		control.direction.x = 0.5
		control.direction.y = -( math.sqrt(3)/2 )
		
		pedestrian.apply_control(control)
		time.sleep(1.0)

		line2 -= 1

	# stop the pedestrian

	control.speed = 0
	pedestrian.apply_control(control)

	# make third line of triangle 
	
	line3 = 1

	while line3 > 0:
		control = carla.WalkerControl()
		control.speed = speed # speed is defined in m/s
		current = pedestrian.get_location()
		control.direction.x = start.location.x - current.x
		control.direction.y = start.location.y - current.y
		
		pedestrian.apply_control(control)
		time.sleep(1.0)

		line3 -= 1
	
	# stop the pedestrian

	control.speed = 0
	pedestrian.apply_control(control)

	# destroy the pedestrian

	pedestrian.destroy()

triangle(random_walker_bp, initial, 10)

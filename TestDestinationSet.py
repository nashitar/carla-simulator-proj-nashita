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
spawn_sidewalk_corner.location = loc(x=190.3622, y=71.4094, z=1)# x=175.29485, y=75.488579, z=0.91) # cross street loc: loc(x=179.50516, y=76.24409, z=0.91) # default: loc(x=190.3622, y=71.4094, z=1)

# set weather in simulation to sunny so the pedestrian is easier to see

weather = carla.WeatherParameters(cloudyness=0.0,precipitation=0.0,sun_altitude_angle=90.0)
world.set_weather(weather)

# spawn the pedestrian at position using a batch of commands

spawn_pedestrian = client.apply_batch_sync([carla.command.SpawnActor(random_walker_bp, spawn_sidewalk_corner)])
# when running carla, there are ninety-one actors that are automatically implemetned 
# into the simulation. therefore, the first pedestrian that is spawned and later the
# first pedestrian controller that is spawned are actors number 92 and 93, respectively.
# will change later because this obviously doesn't work if the script is run a second 
# time on the same simulator because those actors (the new pedestrian and the new 
# pedestrian controller) have different id numbers
pedestrian_id = 92 

# set var person to actor id of spawned pedestrian

person = world.get_actor(pedestrian_id)

# create the controller that will manage the pedestrian automatically
# spawn the controller using controller ai walker blueprint by using a batch of commands
# the controller is created as a child of the walker, so the location passed is (0,0,0)

walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
spawn_controller = client.apply_batch_sync([carla.command.SpawnActor(walker_controller_bp, carla.Transform(), pedestrian_id)])

# set var controller to actor id of spawned pedestrian

controller_id = 93
controller = world.get_actor(controller_id)

# wait for a tick to ensure client receives the last 
# transform of the walkers we have just created

world.wait_for_tick()

# using the controller start the pedestrian and set it's max speed (in m/s)
# using the controller set the locations where each pedestrian should walk to

controller.start()
controller.set_max_speed(0.05)

# the method carla uses to suggest random destination points: controller.go_to_location(world.get_random_location_from_navigation()) 

# method to generate list of random coordinates close to destination coordinate

def RandomPerturbation (coordinate, dev_x, dev_y, dev_z, count=1):

	# pick random coordinates

	x_coordinate = np.random.normal(coordinate.x, dev_x, count)
	y_coordinate = np.random.normal(coordinate.y, dev_y, count)
	z_coordinate = np.random.normal(coordinate.z, dev_z, count)

	# return list of locations using random coordinates
	
	return list(map(lambda coord: loc(x=coord[0],y=coord[1],z=coord[2]), zip(x_coordinate,y_coordinate,z_coordinate))) 

# method to go to approzimate location

def go_to_approx(pedestrian_controller, location):

	# define list of locations

	loc_cloud = []

	loc_cloud = RandomPerturbation(location, 10, 10, 0.1, 100000)
	print(loc_cloud)
	# go to approximate location

	for locs in loc_cloud:
		controller.go_to_location(locs)

	# while True:
	# controller.go_to_location(RandomPerturbation(location, 10, 10, 0.1, 1000))

go_to_approx(controller,loc(x=162.332306, y=75.1117859, z=0.91))


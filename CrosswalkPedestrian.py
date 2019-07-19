import glob
import os
import sys
import time

# sys.path.append('/home/nashita/Downloads/CARLA_0.9.5/PythonAPI/carla/dist/carla-0.9.5-py3.5-linux-x86_64.egg')
sys.path.append('/home/nashita/UnrealEngine_4.22/carla/Dist/CARLA_0.9.5-428-g0ce908d-dirty/LinuxNoEditor/PythonAPI/carla/dist/carla-0.9.5-py3.5-linux-x86_64.egg')

import carla
import argparse
import logging
import random
import decimal

from pprint import PrettyPrinter
pp = PrettyPrinter()

_HOST_ = '127.0.0.1'
_PORT_ = 2000
_SLEEP_TIME_ = 1


client = carla.Client(_HOST_, _PORT_)

LibCarlaVar = carla.libcarla
world = client.get_world()
maps = world.get_map()
tran = LibCarlaVar.Transform
loc = LibCarlaVar.Location
rot = LibCarlaVar.Rotation

client.set_timeout(2.0)
actor_list = []

blueprintsWalkers = world.get_blueprint_library().filter("walker.pedestrian.*")
walker_bp = random.choice(blueprintsWalkers)

recommended_spawn_points = world.get_map().get_spawn_points()
spawn_point = recommended_spawn_points[0]
dest_point = recommended_spawn_points[1]

spawn_points_to_check = []
spawn_points = []
dest_points = []

walkers_list = []
all_id = []
all_actors = []

class CrosswalkPedestrian:
	
	def __init_(self, spawn_x1, spawn_y1, dest_x1, dest_y1, crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1):
		self.spawn_x1 = spawn_x1
		self.spawn_y1 = spawn_y1
		self.dest_x1 = dest_x1
		self.dest_y1 = dest_y1
		self.path_bounds_x1 = path_bounds_x1
		self.crosswalk_y1_start = crosswalk_y1_start
		self.crosswalk_y1_end = crosswalk_y1_end

	# ***** crosswalk 1 *****
	
	# set spawn region

	def spawn_region_1 ():

		spawn_x1_start = 178
		spawn_x1_end_orig = 181
		spawn_x1_end = spawn_x1_end_orig + 1

		spawn_y1_start = 71
		spawn_y1_end_orig = 80 
		spawn_y1_end = spawn_y1_end_orig + 1

		# set spawn position

		spawn_point = recommended_spawn_points[1]
		spawn_point.location = loc(x=179.8672, y=75.88586, z=0.92)

		# choose randomized spawn position

		"""
		for i in range(10): 

			spawn_x1 = decimal.Decimal(random.randrange(spawn_x1_start,spawn_x1_end))
			spawn_y1 = decimal.Decimal(random.randrange(spawn_y1_start,spawn_y1_end))
			
			x1 = float(spawn_x1)
			y1 = float(spawn_y1)

			spawn_point.location = loc(x=x1, y=y1, z=0.91)
			# print (spawn_point.location)

			if(spawn_point.location != None):
				spawn_points_to_check.append(spawn_point)

			count = 0
			
			# make sure spawn points are not repeated 

			for x in spawn_points_to_check:
				if (spawn_point.location == x.location.x):
					count += 1
				elif (spawn_point.location == x.location.y):
					count += 1
				elif (spawn_point.location != x.location.y):
					if (spawn_point.location != x.location.x):
						count += 0

			print (spawn_point.location)
			
			if (count == 0):
				spawn_points.append(spawn_point)
		"""	

		return spawn_point.location
			
	# set destination region

	def dest_region_1 ():
		
		dest_x1_start = 158
		dest_x1_end_orig = 161
		dest_x1_end = (dest_x1_end_orig + 1)

		dest_y1_start = 70
		dest_y1_end_orig = 83
		dest_y1_end = (dest_y1_end_orig + 1)

		# set destination position

		dest_point = recommended_spawn_points[1]
		dest_point.location = loc(x=159.2204, y=76.4056, z=0.92)

		# choose randomized destination position

		"""
		for i in range(10): 

			dest_x1 = decimal.Decimal(random.randrange(dest_x1_start,dest_x1_end))
			dest_y1 = decimal.Decimal(random.randrange(dest_y1_start,dest_y1_end))

			x1 = float(dest_x1) 
			y1 = float(dest_y1) 

			dest_point.location = loc(x=x1, y=y1, z=0.91)

			if(dest_point.location != None):
				dest_points.append(dest_point)
		"""

		return dest_point.location

	# set bounds of crosswalk

	def cross_region_1 ():
		
		crosswalk_x1_start = 161.3
		crosswalk_x1_end = 176.8

		crosswalk_y1_start = 74.3
		crosswalk_y1_end = 76.4

		jaywalk_y1_endpair = 71.2
		jaywalk_y1_startpair = 78.1

	cross_region_1 ()

	# ***********************

	# set path x bound

	def path_bound_x ():

		path_bounds_x1 = [crosswalk_x1_start,crosswalk_x1_end]

	# set walking time range

class Lawful(CrosswalkPedestrian):

	# ***** parameters *****
	# 1. pedestrian walks within the bounds of the crosswalk
	# 2. pedestrian walks when car is stopped at stop sign
	# 3. pedestrian walks when traffic light is red (walk sign is white)
	# 4. randomized path movement

	def __init_(self, spawn_x1, spawn_y1, dest_x1, dest_y1, crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1):
		super(Lawful,self).__init__(spawn_x1, spawn_y1, dest_x1, dest_y1, crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1)

		super(Lawful,self).spawn_region_1 ()
		super(Lawful,self).dest_region_1 ()
		super(Lawful,self).cross_region_1 ()

		super(Lawful,self).spawn_position ()
		super(Lawful,self).dest_position ()

		path_bounds_y1 = [crosswalk_y1_start,crosswalk_y1_end]

	def path_1 ():

		# ***********************
		# pedestrian must stay 
		# within the constraints 
		# of path_bounds_x1 and 
		# path_bounds_y1
		# ***********************

		print ("path 1")

	print ("")

class Jaywalkers(CrosswalkPedestrian):

	# ***** parameters *****
	# 1. pedestrian walks outside the bounds of the crosswalk
	# 2. pedestrian walks when car is not stopped at stop sign
	# 3. pedestrian walks when traffic light is yellow or green (walk sign is red)
	# 4. randomized path movement

	def __init_(self, crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1):
		super(Jaywalkers,self).__init__(crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1)

		super(Jaywalkers,self).spawn_region_1 ()
		super(Jaywalkers,self).dest_region_1 ()
		super(Jaywalkers,self).cross_region_1 ()

		super(Jaywalkers,self).spawn_position ()
		super(Jaywalkers,self).dest_position ()

		path_bounds_y01 = [crosswalk_y1_end,jaywalk_y1_endpair]
		path_bounds_y11 = [jaywalk_y1_startpair,crosswalk_y1_start]
		spawn_point.location = loc(x=x1, y=y1, z=0.91)
	
	def path_1 ():

		# ***********************
		# pedestrian must stay 
		# within the constraints 
		# of path_bounds_x1 and 
		# path_bounds_y01 and
		# path_bounds_y11
		# ***********************

		print ("path 1")

	print ("")


class Hurried(CrosswalkPedestrian):

	# ***** parameters *****
	# 1. pedestrian spends range of time within the bounds of crosswalk
	# 2. pedestrian spends rest of time outside bounds of crosswalk
	# 3. pedestrian may start when walk sign is red (traffic light is green or 
	#    yellow) but finishes journey when walk sign is white (or vise-versa)
	# 4. randomized path movement
	
	def __init_(self, spawn_x1, spawn_y1, dest_x1, dest_y1, crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1):
		super(Hurried,self).__init__(spawn_x1, spawn_y1, dest_x1, dest_y1, crosswalk_y1_start, crosswalk_y1_end, path_bounds_x1)

		super(Hurried,self).spawn_region_1 ()
		super(Hurried,self).dest_region_1 ()
		super(Hurried,self).cross_region_1 ()

		super(Hurried,self).spawn_position ()
		super(Hurried,self).dest_position ()

		spawn_point.location = loc(x=x1, y=y1, z=0.91)

def main ():

	while(True): 
		t = world.get_spectator().get_transform()
		coordinate_str = "(x,y,z) = ({},{},{})".format(t.location.x, t.location.y,t.location.z)
		print (coordinate_str)
		time.sleep(_SLEEP_TIME_)			

	while True:
		world.wait_for_tick()

main ()
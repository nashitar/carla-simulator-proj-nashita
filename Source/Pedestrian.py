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

class Pedestrian:

	def __init__ (self, location):
		
		# define spawn point

		recommended_spawn_points = world.get_map().get_spawn_points() # spawn points from carla
		spawn_point = recommended_spawn_points[1] # used to set rotation class before location is changed
		spawn_point.location = location

		# create lists to contain values that will later be plotted

		self.plot_values = []
		self.control_input = []
		self.control_output = []

		# randomly define blueprint for pedestrian

		bp = random.choice(blueprintsWalkers)

		# define a pedestrian to spawn at the initial location

		self.pedestrian = world.spawn_actor(bp, spawn_point)
		world.wait_for_tick()

	def _go_to_location (self, final, tolerance=1, speed=5):

		# set initial values for pid controller and create control 
		# variable in order to track and control pedestrain movement 
		# and set basic value for speed 

		pid = PID(Kd=0.1, Ki=0.01, setpoint=0, output_limits=(-0.8, 0.8))
		control = carla.WalkerControl()
		control.speed = speed # speed is defined in m/s
		
		# tell the pedestrian to move until the destination is reached	

		while True: 

			# ************************************************
			# sense
			# ************************************************

			# get value of pedestrian location and velocity

			location = self.pedestrian.get_location()
			velocity = self.pedestrian.get_velocity()
			
			# assign variable DL to the vector from the pedestrian's 
			# initial location to the pedestrian's destination location

			DL = complex(final.x-location.x,final.y-location.y)

			# assign variable H to the heading of the pedestrian

			H = complex(velocity.x, velocity.y)

			# calculate the error between the pedestrian's current heading
			# and their desired heading. use if statement in order to avoid
			# divide by zero error

			if (la.norm([H.real, H.imag]) == 0):
				theta_error = 0
			else:
				
				# check the direction of vector DL with respect to the 
				# pedestrian's heading in order to derive the sign of the error

				if (DL/H).imag > 0:
					sign = -1
				else:
					sign = 1
				
				# calculate the angle of the error

				theta_error = sign*math.acos(
					np.dot(
						[final.x-location.x,final.y-location.y],
						[H.real, H.imag]) /
					(la.norm([final.x-location.x,final.y-location.y]) *
						la.norm([H.real, H.imag])))
			
			# if location is reached, stop running the loop
			
			if la.norm([final.x-location.x,final.y-location.y]) <= tolerance:
				break

			# add the pedestrian's current location to a list 
			# so that it can later be plotted

			self.plot_values.append(self.pedestrian.get_location())
			
			# if the pedestrian is not moving and/or moving abnormally 
			# slow, move it up in case the reason for the lack of speed 
			# is that the pedestrian needs to get on the sidewalk

			if (math.sqrt(math.pow(velocity.x,2)+math.pow(velocity.y,2))) < 0.4:
				self.pedestrian.set_location(loc(self.pedestrian.get_location().x, y=self.pedestrian.get_location().y, z=1.2))

			# ************************************************
			# compute
			# ************************************************

			# pid controller for angle update

			theta_control = pid(theta_error)	

			# record the control input and the control output so
			# that the data can later be graphed to compare them

			self.control_input.append(theta_error)
			self.control_output.append(theta_control)

			# ************************************************
			# actuate
			# ************************************************

			# create rotation matrix to shift the heading of the pedestrian
			# based on the theta control found by the pid controller

			rotation = np.array(((np.cos(theta_control), -1.0*np.sin(theta_control)), (np.sin(theta_control), np.cos(theta_control))))
			heading = np.array((H.real,H.imag))

			# calculate the new heading of the pedestrian by rotating the 
			# previous heading

			new_heading = rotation.dot(heading) + np.random.normal(scale=0.05, size=(2,))
			new_heading /= la.norm(new_heading)

			# set the new direction of the pedestrian

			control.direction.y = new_heading[1]
			control.direction.x = new_heading[0]

			# apply the values set to the control variable to the pedestrian

			self.pedestrian.apply_control(control)
			world.wait_for_tick()

		# stop the pedestrian

		control.speed = 0
		self.pedestrian.apply_control(control)

	# destroy the pedestrian once complete

	def destroy (self):

		self.pedestrian.destroy()

	# tell pedestrian to use a set of points as waypoints and follow a path
	
	def _follow_path (self, coordinates, tolerance=1, speed=[1]):

		list_of_speeds = [speed[0] for _ in range((len(coordinates))-1)]

		if (len(speed) == 1):
			for i in range((len(coordinates))-1):
				list_of_speeds.append(speed[0])
		elif (len(coordinates) - len(speed)) == 1:
			list_of_speeds = speed
		else:
			for i in range((len(coordinates))-1):
				list_of_speeds.append(speed[0])
		for i in range(1, (len(coordinates))-1):
			self._go_to_location(coordinates[i+1], tolerance, list_of_speeds[i])

	# handle SIGINT so pedestrian is destroyed when crtl+c is pressed

	def signal_handler (self, sig, frame):
		self.pedestrian.destroy()
		sys.exit(0)

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

from ..Source.LawfulCrosswalkPedestrian import LawfulCrosswalkPedestrian

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

# test

x = open('x_law.txt', 'a')
y = open('y_law.txt', 'a')

inputs = open('inputs.txt', 'w')
outputs = open ('outputs.txt', 'w')

try:
	for i in range(100):

		coordinates = LawfulCrosswalkPedestrian.path(177.5, 180, 158, 161, 74, 76.5, 74, 76.5)
		pedestrian = LawfulCrosswalkPedestrian(coordinates[0])

		signal.signal(signal.SIGINT, pedestrian.signal_handler)

		pedestrian._follow_path(coordinates, 0.5, [1.0])

		######################################
		# grapth the path of the pedestrian
		######################################

		coordinates = pedestrian.plot_values

		for coordinate in coordinates:
			if (coordinate.x != 0.0 and coordinate.y != 0.0 and abs(coordinate.x) > 0.0 and abs(coordinate.y) > 0.0):
				x.write(str(coordinate.x))
				x.write('\n')
				y.write(str(coordinate.y))
				y.write('\n')
		
		x.write('\n')
		y.write('\n')

		################################################
		# graph the control input vs. the control output
		################################################

		input_list = pedestrian.control_input
		output_list = pedestrian.control_output

		for input in input_list:
			inputs.write(str(input))
			inputs.write('\n')

		for output in output_list:
			outputs.write(str(output))
			outputs.write('\n')

		print (i)
		
		# destroy pedestrian

		pedestrian.destroy()

finally:

	x.close()
	y.close()

	inputs.close()
	outputs.close()

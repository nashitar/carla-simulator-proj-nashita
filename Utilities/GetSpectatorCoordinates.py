# import necessary packages  

import glob
import os
import sys
import time
from ..Configuration import carla_path

sys.path.append(carla_path)

import carla
import argparse
import logging

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

# print spectator coordinates while true

while(True): 
	transform = world.get_spectator().get_transform()
	coordinates = "(x,y,z) = ({},{},{})".format(transform.location.x, transform.location.y,transform.location.z)
	print (coordinates)
	time.sleep(_SLEEP_TIME_)

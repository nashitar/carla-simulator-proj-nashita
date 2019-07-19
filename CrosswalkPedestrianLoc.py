# july 9, 2019
# code to set custom spawn location for crasswalk pedestrians

import glob
import os
import sys
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import argparse
import logging
import random
import decimal

_HOST_ = '127.0.0.1'
_PORT_ = 2000
_SLEEP_TIME_ = 1

class walk:

	argparser = argparse.ArgumentParser(
		description=__doc__)
	argparser.add_argument(
		'--host',
		metavar='H',
		default='127.0.0.1',
		help='IP of the host server (default: 127.0.0.1)')
	argparser.add_argument(
		'-p', '--port',
		metavar='P',
		default=2000,
		type=int,
		help='TCP port to listen to (default: 2000)')
	argparser.add_argument(
		'-n', '--number-of-walkers',
		metavar='N',
		default=10,
		type=int,
		help='number of walkers (default: 10)')
	argparser.add_argument(
		'-d', '--delay',
		metavar='D',
		default=2.0,
		type=float,
		help='delay in seconds between spawns (default: 2.0)')
	argparser.add_argument(
		'--safe',
		action='store_true',
		help='avoid spawning walkers prone to accidents')
	args = argparser.parse_args()

	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


	client = carla.Client(_HOST_, _PORT_)
	libcar = carla.libcarla
	client.set_timeout(2.0)
	actor_list = []
	world = client.get_world()
	maps = world.get_map()
	spawn = maps.get_spawn_points()
	tran = libcar.Transform
	loc = libcar.Location
	rot = libcar.Rotation

	try:
		bp = random.choice(world.get_blueprint_library().filter('walker.*'))
		transform = world.get_map().get_spawn_points()[0]

		spawn_x1_start = 176.5*10
		spawn_x1_end_orig = 180.1*10
		spawn_x1_end = spawn_x1_end_orig + 1

		spawn_y1_start = 70.00*10
		spawn_y1_end_orig = 80.00*10
		spawn_y1_end = spawn_y1_end_orig + 1

		spawn_x1 = decimal.Decimal(random.randrange(spawn_x1_start,spawn_x1_end))/10
		x1 = float(spawn_x1) * 1.0

		spawn_y1 = decimal.Decimal(random.randrange(spawn_y1_start,spawn_y1_end))/10
		y1 = float(spawn_y1) * 1.0

		recommended_spawn_points = world.get_map().get_spawn_points()
		spawn_point = recommended_spawn_points[1]
		print ("spawn point", spawn_point.location)

		spawn_point.location = loc(x=x1, y=y1, z=0)

		print ("spawn point", spawn_point.location)
		
		#
		# print all carla suggested spawn points
		#
		#
		# print (len(world.get_map().get_spawn_points()))
		# for x in range(random.randint(0,200)):
		# 	print (world.get_map().get_spawn_points()[x])
		#

		transform = tran(spawn_point.location, rot(yaw=180))
		pedestrian = world.spawn_actor(bp, transform)

		while(True):  
			control = carla.WalkerControl()
			control.speed = 0.9
			control.direction.y = 1
			control.direction.x = 0
			pedestrian.apply_control(control)
			time.sleep(1)

			control.jump
			pedestrian.apply_control(control)
			time.sleep(1)

			t = world.get_spectator().get_transform()
			coordinate_str = "(x,y,z) = ({},{},{})".format(t.location.x, t.location.y,t.location.z)
			print (coordinate_str)
			time.sleep(_SLEEP_TIME_)			

		SpawnActor = carla.command.SpawnActor
		SetAutopilot = carla.command.SetAutopilot
		FutureActor = carla.command.FutureActor

		batch = []

		for response in client.apply_batch_sync(batch):
			if response.error:
				logging.error(response.error)
			else:
				actor_list.append(response.actor_id)

		while True:
			world.wait_for_tick()

	finally:
		print ("done!")

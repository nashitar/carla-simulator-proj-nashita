import glob
import os
import sys

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

def main():
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

	

    actor_list = []
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)

try:
    world = client.get_world()
    bp = random.choice(world.get_blueprint_library().filter('walker.*'))
    
    transform = world.get_map().get_spawn_points()[0]
	pedestrian = world.spawn_actor(bp, transform)

	while True: 
	    control = carla.WalkerControl()
	    control.speed = 0.9
	    control.direction.y = 1
	    control.direction.x = 0
  	    control.direction.x = 0
	    pedestrian.apply_control(control)
	    time.sleep(1)

	    control.jump
	    pedestrian.apply_control(control)
	    time.sleep(1)
	    
	    i+= 1

	"""

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        world.try_spawn_actor(blueprint, spawn_point)

        control = carla.WalkerBoneControl()
        first_tuple = ('crl_hand__R', carla.Transform(rotation=carla.Rotation(roll=90)))
        second_tuple = ('crl_hand__L', carla.Transform(rotation=carla.Rotation(roll=90)))
        control.bone_transforms = [first_tuple, second_tuple]
        world.player.apply_control(control)

        if args.number_of_walkers < number_of_spawn_points:
            random.shuffle(spawn_points)
        elif args.number_of_walkers > number_of_spawn_points:
            msg = 'requested %d walkers, but could only find %d spawn points'
            logging.warning(msg, args.number_of_walkers, number_of_spawn_points)
            args.number_of_walkers = number_of_spawn_points
	
	"""

        # @todo cannot import these directly.
        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        FutureActor = carla.command.FutureActor

        batch = []

        """        
	for n, transform in enumerate(spawn_points):
            if n >= args.number_of_walkers:
                break
            blueprint = random.choice(blueprints)
            blueprint.set_attribute('role_name', 'autopilot')
            batch.append(SpawnActor(blueprint, transform).then(SetAutopilot(FutureActor, True)))
        """

        for response in client.apply_batch_sync(batch):
            if response.error:
                logging.error(response.error)
            else:
                actor_list.append(response.actor_id)

        print('spawned %d walkers, press Ctrl+C to exit.' % len(actor_list))

        while True:
            world.wait_for_tick()

    finally:

        print('\ndestroying %d actors' % len(actor_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')



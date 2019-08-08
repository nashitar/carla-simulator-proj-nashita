# import necessary packages

import signal
import random
import math
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plot

# create lists to store x and y coordinates for plotting

x_coordinate = []
y_coordinate = []

# open the files that contain the x and y values of the coordinates

x = open('x_jay.txt') # change name of file
y = open('y_jay.txt') # change name of file

# open the files that will store the control inputs and outputs for plotting

inputs = open('inputs.txt')
outputs = open ('outputs.txt')

# create lists to store the control inputs and outputs for plotting

input_list = []
output_list = []

try:

	# read the x coordinate file

	read = x.readlines()
	
	# append the x coordinates to the list

	for lines in read:
		if(not(len(lines)>=20 or len(lines)<=2)):
			x_coordinate.append(float(lines))
	
	# print the minimum and maximum values of the x coordinates

	print("x:", min(x_coordinate), max(x_coordinate))

	# read the y coordinate file

	read = y.readlines()
	
	# append the y coordinates to the list

	for lines in read:
		if (not(len(lines)>=20 or len(lines)<=2)):
			y_coordinate.append(float(lines))
	
	# print the minimum and maximum values of the y coordinates

	print("y:", min(y_coordinate), max(y_coordinate))

	# make sure that the lengths of the lists are equal

	print("lengths:", "x:", len(x_coordinate), " y:", len(y_coordinate))
	# assert(len(x_coordinate)==len(y_coordinate))

	# generate the heat map

	heatmap, xedges, yedges = np.histogram2d(x_coordinate, y_coordinate)
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	plot.clf()
	plot.title('Heat Map')
	plot.imshow(heatmap, extent=extent)
	plot.show()

	# read the control input file

	read = inputs.readlines()
	
	# append the control inputs to the list

	for lines in read:
		input_list.append(float(lines))

	# read the control output file

	read = outputs.readlines()
	
	# append the control outputs to the list
	
	for lines in read:
		output_list.append(float(lines))

	# make sure that the lengths of the input list and output list are equal

	assert(len(input_list)==len(output_list))
	
	# plot the control values

	plot.plot(input_list)
	plot.plot(output_list)

	plot.show()

finally:

	# close the files

	x.close()
	y.close()

	inputs.close()
	outputs.close()
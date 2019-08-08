# carla-simulator-proj-nashita 
***

## Experiments
***

* **CollectDataLawful.py** 

Creates a path for the pedestrian to follow by calling the path method of LawfulCrosswalkPedestrian.py and inputting the coordinates of the bounds of the crosswalk and then creates a pedestrian object by calling the LawfulCrosswalkPedestrian and inputting the first coordinate in the path that was created earlier. Then, while the pedestrian follows the created path, the coordinates it passes through are recorded in two separate text files, one for the x values and one for the y values. The control inputs and outputs are also collected while the coordinates are being collected and then written into their own files.

* **CollectDataJaywalking.py** 

Creates a path for the pedestrian to follow by calling the path method of JaywalkingCrosswalkPedestrian.py and inputting the coordinates of the bounds of the crosswalk and then creates a pedestrian object by calling the JaywalkingCrosswalkPedestrian and inputting the first coordinate in the path that was created earlier. Then, while the pedestrian follows the created path, the coordinates it passes through are recorded in two separate text files, one for the x values and one for the y values. The control inputs and outputs are also collected while the coordinates are being collected and then written into their own files.

* **CollectDataHurried.py** 

Creates a path for the pedestrian to follow by calling the path method of HurriedCrosswalkPedestrian.py and inputting the coordinates of the bounds of the crosswalk and then creates a pedestrian object by calling the HurriedCrosswalkPedestrian and inputting the first coordinate in the path that was created earlier. Then, while the pedestrian follows the created path, the coordinates it passes through are recorded in two separate text files, one for the x values and one for the y values. The control inputs and outputs are also collected while the coordinates are being collected and then written into their own files.

* **GenerateGraphs.py**

Reads the files that were created in the CollectData files in order to create a heat map and a graph of the control inputs vs. the control outputs 

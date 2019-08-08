# carla-simulator-proj-nashita
***

## Source
***

* **Pedestrian.py**

Pedestrian defines the spawn point and defines a pedestrian to spawn at the initial location. It also creates lists to contain values that will later be plotted. In the private go_to_location function, Pedestrian sets initial values for pid controller and creates control variable in order to track and control pedestrain movement and sets basic value for speed. It then enters a control loop where it recordes the control inputs and outputs and the pedestrians coordinates and actuates until the pedestrian reaches the destination. Pedestrian is used outside of itself in order to tell pedestrian to use a set of points (created elsewhere) as waypoints and follow a path. Pedestrian has a desroy function and also handles SIGINT so pedestrian is destroyed when `crtl+c` is pressed.

* **PedestrianTrianglePath.py**

The pedestrian spawns at a specific location and follows a path with three points in order to walk in an equilateral triangle. The directions of the first two lines are based on the angles of an equilateral triangle, but the third line is derived mathematically based on the current and desired locations in order to account for topographical differenced.

* **CrosswalkPedestrian.py**

Selects a spawn point along the first sidewalk and if the selected spawn point is far from the crosswalk, more points along the sidewalk have to be added to the list of coordinates so that the pedestrian doesn't get stuck anywhere. CrosswalkPedestrian then has functions to return the transition point of the pedestrian by randomly selecting a point along a gaussian distribution, return the point on the sidewalk close to the transition point and the destination point of the pedestrian by randomly selecting a point along a uniform distribution, and select and return between two and four locations along the path with some measure of randomness.

* **LawfulCrosswalkPedestrian.py**

***parameters***
1. pedestrian walks within the bounds of the crosswalk
2. pedestrian walks when car is stopped at stop sign
3. pedestrian walks when traffic light is red (walk sign is white)
4. randomized path movement

The path function uses the various functions within CrosswalkPedestrian in order to generate a randomized list of coordinates (a path) that the pedestrian can follow, while following their intended bahavior.

* **JaywalkingCrosswalkPedestrian.py**

***parameters***
1. pedestrian walks outside the bounds of the crosswalk
2. pedestrian walks when car is not stopped at stop sign
3. pedestrian walks when traffic light is yellow or green (walk sign is red)
4. randomized path movement

The path function uses the various functions within CrosswalkPedestrian in order to generate a randomized list of coordinates (a path) that the pedestrian can follow, while following their intended bahavior.

* **HurriedCrosswalkPedestrian.py**

***parameters***
1. pedestrian spends range of time within the bounds of crosswalk
2. pedestrian spends rest of time outside bounds of crosswalk
3. pedestrian may start when walk sign is red (traffic light is green or yellow) but finishes journey when walk sign is white (or vise-versa)
4. randomized path movement

The path function uses the various functions within CrosswalkPedestrian in order to generate a randomized list of coordinates (a path) that the pedestrian can follow, while following their intended bahavior.
import sys
import math
import time
import os

import interop


usern = 'testuser'
passw = 'testpass'
youareL = 'http://10.0.0.5:8000'

# pathName = 'D:/MUAS/AutoPilot/MissionData/'


missionFileLoc = "../Mission_data.txt"

staticObjFileloc = '../static_obstacles.txt'

movingObjFileLoc = '../moving_obstacles.txt'

client = interop.Client(url=youareL, username=usern, password=passw)

missions = client.get_missions()


with open(missionFileLoc,"w") as missionFile:
	missionFile.write("off_axis_target_pos")
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].off_axis_odlc_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].off_axis_odlc_pos.longitude))
	missionFile.write(str('\n'))




		

stationary_obstacles, moving_obstacles = client.get_obstacles()

with open(staticObjFileloc,"w") as staticObjFile:
	for j in range(len(stationary_obstacles)):
		if(j != 0):
			staticObjFile.write('\n')
		staticObjFile.write(str(stationary_obstacles[j].latitude))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].longitude))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].cylinder_height))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].cylinder_radius))
		



timelast = time.time()
while(True):

	stationary_obstacles, moving_obstacles = client.get_obstacles()
	print(moving_obstacles)
	with open(movingObjFileLoc,"w") as movingObjFile:
		for i in range(len(moving_obstacles)):
			if(i != 0):
				movingObjFile.write('\n')	
			movingObjFile.write(str(moving_obstacles[i].latitude))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].longitude))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].altitude_msl))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].sphere_radius))

	
	while(time.time()-timelast < .1):
		time.sleep(.005)
	timelast = time.time()

	